import functools
import os
import threading
from concurrent.futures import Future, ThreadPoolExecutor
import time
from typing import Any, Dict, List, Optional, TypeVar
from warnings import warn

import nanoid
import requests
from langwatch.types import (
    BaseSpan,
    ErrorCapture,
    RAGChunk,
    RAGSpan,
    Span,
    SpanTimestamps,
    SpanTypes,
    CollectorRESTParams,
    TraceMetadata,
)
from langwatch.utils import (
    SerializableAndPydanticEncoder,
    autoconvert_typed_values,
    capture_exception,
    milliseconds_timestamp,
)
from retry import retry

import langwatch
import contextvars  # Import contextvars module


class ContextSpan:
    span_id: str
    parent: Optional["ContextSpan"] = None
    name: Optional[str]
    type: SpanTypes
    input: Any
    output: Optional[Any] = None
    started_at: int

    def __init__(
        self,
        span_id: str,
        name: Optional[str],
        type: SpanTypes = "span",
        input: Any = None,
    ) -> None:
        self.span_id = span_id
        self.name = name
        self.type = type
        self.input = input

        current_tracer = current_tracer_var.get()

        if current_tracer:
            if current_tracer.current_span:
                self.parent = current_tracer.current_span
            current_tracer.current_span = self
        else:
            warn("No current tracer found, some spans will not be sent to LangWatch")

        self.started_at = milliseconds_timestamp()

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, exc_value: Optional[BaseException], _exc_traceback):
        error: Optional[ErrorCapture] = (
            capture_exception(exc_value) if exc_value else None
        )
        finished_at = milliseconds_timestamp()

        current_tracer = current_tracer_var.get()
        if current_tracer:
            span_id = self.span_id  # TODO: test?
            current_tracer.append_span(
                self.create_span(span_id, current_tracer, error, finished_at)
            )

            current_tracer.current_span = self.parent

    def create_span(
        self,
        span_id: str,
        context_tracer: Any,
        error: Optional[ErrorCapture],
        finished_at: int,
    ) -> BaseSpan:
        return BaseSpan(
            type=self.type,
            name=self.name,
            span_id=span_id,
            parent_id=self.parent.span_id if self.parent else None,
            trace_id=context_tracer.trace_id,
            input=autoconvert_typed_values(self.input) if self.input else None,
            outputs=([autoconvert_typed_values(self.output)] if self.output else []),
            error=error,
            metrics=None,
            timestamps=SpanTimestamps(
                started_at=self.started_at, finished_at=finished_at
            ),
        )


class ContextRAGSpan(ContextSpan):
    contexts: List[RAGChunk]

    def __init__(
        self,
        id: str,
        name: Optional[str],
        input: Any = None,
        contexts: List[RAGChunk] = [],
    ) -> None:
        super().__init__(id, name, type="rag", input=input)
        self.contexts = contexts

    def create_span(
        self,
        id: str,
        context_tracer: Any,
        error: Optional[ErrorCapture],
        finished_at: int,
    ) -> RAGSpan:
        span: Any = super().create_span(id, context_tracer, error, finished_at)
        rag_span: RAGSpan = {**span, "type": "rag", "contexts": self.contexts}

        return rag_span


def create_span(
    name: Optional[str] = None, type: SpanTypes = "span", input: Any = None
):
    return ContextSpan(
        span_id=f"span_{nanoid.generate()}", name=name, type=type, input=input
    )


def capture_rag(
    contexts: List[RAGChunk] = [],
    input: Optional[str] = None,
    name: str = "RetrievalAugmentedGeneration",
):
    return ContextRAGSpan(
        id=f"span_{nanoid.generate()}", name=name, input=input, contexts=contexts
    )


def span(name: Optional[str] = None, type: SpanTypes = "span"):
    def _span(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            all_args = (
                {str(index): item for index, item in enumerate(args)} if args else {}
            )
            if kwargs:
                all_args.update(kwargs)

            with create_span(
                name=(name or func.__name__), type=type, input=all_args
            ) as span:
                output = func(*args, **kwargs)
                span.output = output
                return output

        return wrapper

    return _span


def get_current_tracer():
    return current_tracer_var.get()


executor = ThreadPoolExecutor(max_workers=10)


class BaseContextTracer:
    sent_once = False
    scheduled_send: Optional[Future[None]] = None
    current_span: Optional[ContextSpan] = None

    def __init__(
        self,
        trace_id: Optional[str],
        metadata: Optional[TraceMetadata],
    ):
        self.spans: Dict[str, Span] = {}
        self.trace_id = trace_id or f"trace_{nanoid.generate()}"
        self.metadata = metadata

    def __enter__(self):
        self.token = current_tracer_var.set(self)
        return self

    def __exit__(self, _type, _value, _traceback):
        self.delayed_send_spans()
        current_tracer_var.reset(self.token)

    def delayed_send_spans(self):
        self._add_finished_at_to_missing_spans()

        if "PYTEST_CURRENT_TEST" in os.environ:
            # Keep on the same thread for tests
            self.send_spans_sync()
            return

        def run_in_thread():
            time.sleep(1)  # wait for other spans to be added
            self.sent_once = True
            self.send_spans_sync()

        if self.scheduled_send and not self.scheduled_send.done():
            self.scheduled_send.cancel()

        self.scheduled_send = executor.submit(run_in_thread)

    def send_spans_sync(self):
        send_spans(
            CollectorRESTParams(
                trace_id=self.trace_id,
                metadata=self.metadata,
                spans=list(self.spans.values()),
            )
        )

    def append_span(self, span: Span):
        span["span_id"] = span.get("span_id", f"span_{nanoid.generate()}")
        self.spans[span["span_id"]] = span
        if self.sent_once:
            self.delayed_send_spans()  # send again if needed

    def get_parent_id(self):
        if self.current_span:
            return self.current_span.span_id
        return None

    # Some spans get interrupted in the middle, for example by an exception, and we might end up never tagging their finish timestamp, so we do it here as a fallback
    def _add_finished_at_to_missing_spans(self):
        for span in self.spans.values():
            if "timestamps" in span and (
                "finished_at" not in span["timestamps"]
                or span["timestamps"]["finished_at"] == None
            ):
                span["timestamps"]["finished_at"] = milliseconds_timestamp()


current_tracer_var = contextvars.ContextVar[Optional[BaseContextTracer]](
    "current_tracer", default=None
)


@retry(tries=5, delay=0.5, backoff=3)
def send_spans(data: CollectorRESTParams):
    if len(data["spans"]) == 0:
        return
    if not langwatch.api_key:
        warn(
            "LANGWATCH_API_KEY is not set, LLMs traces will not be sent, go to https://langwatch.ai to set it up"
        )
        return
    import json

    # TODO: replace this with httpx, don't forget the custom SerializableAndPydanticEncoder encoder
    response = requests.post(
        langwatch.endpoint + "/api/collector",
        data=json.dumps(data, cls=SerializableAndPydanticEncoder),
        headers={
            "X-Auth-Token": str(langwatch.api_key),
            "Content-Type": "application/json",
        },
    )
    if response.status_code == 429:
        json = response.json()
        if "message" in json and "ERR_PLAN_LIMIT" in json["message"]:
            warn(json["message"])
        else:
            warn("Rate limit exceeded, dropping message from being sent to LangWatch")
    else:
        response.raise_for_status()
