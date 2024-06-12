import abc
from contextlib import contextmanager
from logging import Logger
from typing import (
    Any,
    Callable,
    Iterator,
    Optional,
    Sequence,
    TYPE_CHECKING,
    Union,
)

from opentelemetry import context as context_api
from opentelemetry import trace as trace_api
from opentelemetry.trace import SpanContext, Tracer
from opentelemetry.trace.span import Span
from opentelemetry.util import types

from .add_rag_event_interface import AddRagEventInterface
from ..common.types import RagFlowType

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

class LastMileTracer(AddRagEventInterface, Tracer):
    """
    A tracer proxy around OpenTelemetry tracer. It has 3 main functionalities:

    1. Create span data and attach it to the tracer. This is the same API as
        OpenTelemetry's tracer:
            a. `trace_function()`
            b. `start_as_current_span()`
            c. `start_span()`
    2. Add RAG events and store their states alongside the trace data:
            a. `add_rag_event_for_span()`
                i: See all the different types of RAG events in
                    `AddRagEventInterface` (ex: `add_query_event()`)
            b. `add_rag_event_for_trace()`
    3. Register a dictionary of parameters to be logged and associated with
        the trace data. The methods for this are:
            a. `register_param()`
            b. `register_params()`
            c. `get_params()`
            d. `clear_params()`
    """

    @abc.abstractmethod
    def trace_function(
        self,
        name: Optional[str] = None,
        context: Optional[Union[context_api.Context, SpanContext, str]] = None,
        kind: trace_api.SpanKind = trace_api.SpanKind.INTERNAL,
        attributes: types.Attributes = None,
        links: Optional[Sequence[trace_api.Link]] = None,
        start_time: Optional[int] = None,
        record_exception: bool = True,
        set_status_on_exception: bool = True,
        end_on_exit: bool = True,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...

    @abc.abstractmethod
    @contextmanager
    def start_as_current_span(  # pylint: disable=too-many-locals
        self,
        name: str,
        context: Optional[Union[context_api.Context, SpanContext, str]] = None,
        kind: trace_api.SpanKind = trace_api.SpanKind.INTERNAL,
        attributes: types.Attributes = None,
        links: Optional[Sequence[trace_api.Link]] = None,
        start_time: Optional[int] = None,
        record_exception: bool = True,
        set_status_on_exception: bool = True,
        end_on_exit: bool = True,
    ) -> Iterator[Span]:
        """
        Same API as opentelemetry.trace.Tracer.start_as_current_span
        But also allows a SpanContext to be passed in as the context parameter.
        If context is a string, it is assumed to be a serialized SpanContext

        Just like the OpenTelemetry API, this method can be used as both a
        context manager and a decorator.
        ```
        from opentelemetry import trace as trace_api
        from lastmile_eval.rag.debugger.tracing import get_lastmile_tracer

        tracer: LastMileTracer = get_lastmile_tracer(
            tracer_name="<my-tracer-name>",
            lastmile_api_token="<my-api-token>"
        )

        # Context Manager
        with tracer.start_as_current_span("my-span") as span:
            span.set_attribute("<my-key>", "<my-value>")

        # Decorator
        @tracer.start_as_current_span("my-span")
        def my_function():
            span = trace_api.get_current_span()
            span.set_attribute("<my-key>", "<my-value>")
        ```

        If you are using this as a decorator instead of context manager, it's
        recommended to use `@traced(tracer)` instead since that also logs the
        wrapped method's inputs and outputs as span attributes:
        ```
        from lastmile_eval.rag.debugger.tracing.decorators import traced

        # Recommended way of decorating a function
        @traced(tracer)
        def my_function(my_arg: str):
            # my_arg is automatically added to the span attributes

            span = trace_api.get_current_span()
            span.set_attribute("<my-key>", "<my-value>")
            ...

            # output_value is automatically added to the span attributes too
            return output_value
        ```
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def start_span(
        self,
        name: str,
        context: Optional[Union[context_api.Context, SpanContext, str]] = None,
        kind: trace_api.SpanKind = trace_api.SpanKind.INTERNAL,
        attributes: types.Attributes = None,
        links: Sequence[trace_api.Link] = (),
        start_time: Optional[int] = None,
        record_exception: bool = True,
        set_status_on_exception: bool = True,
    ) -> Span:
        """
        Same API as opentelemetry.trace.Tracer.start_span
        But also allows a SpanContext to be passed in as the context parameter.
        If context is a string, it is assumed to be a serialized SpanContext
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def get_params(self) -> dict[str, Any]:
        """
        Returns the params_dict that contains all the parameters that have been
        registered with a trace so far.

        If this is called outside of an active trace, it will return the
        global params dict that contains K-V pairs that will be common in all
        future traces (if they haven't been cleared via `clear_params()`)
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def register_param(
        self,
        key: str,
        value: Any,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """
        Define the parameter K-V pair to save for the current trace instance.

        If this is called outside of an active trace, it will save this into
        a global params dict that contains K-V pairs that will be common in all
        future traces (if they haven't been cleared via `clear_params()`)

        @param key (str): The name of the parameter to be saved
        @param value (Any): The value of the parameter to be saved
        @param should_also_save_in_span (bool): Whether to also save this K-V
            pair in the current span attributes data. Defaults to true
        @param span Optional(Span): The span to save the K-V pair in
            addition to regular paramSet. This can be helpful for debugging
            when going through the trace. Only has an effect if
            should_also_save_in_span is true. Defaults to
            `trace_api.get_current_span()` which is the most recent span
            generated by calling tracer.start_as_current_span
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def register_params(
        self,
        params: dict[str, Any],
        should_overwrite: bool = False,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """
        Helper function for individually calling `register_param`, with the
        added capability of clearing existing parameters if they exist.

        If this is called outside of an active trace, it will save these into
        a global params dict that contains K-V pairs that will be common in all
        future traces (if they haven't been cleared via `clear_params()`)

        @param params dict[str, Any]: The parameter K-V pairs to save
        @param should_also_save_in_span (bool): Whether to also save this K-V
            pair in the current span attributes data. Defaults to true
        @param should_overwrite (bool): Whether to clear existing parameters
            if they already exist. Defaults to false.
        @param span Optional(Span): The span to save the K-V pair in
            addition to regular paramSet. This can be helpful for debugging
            when going through the trace. Only has an effect if
            should_also_save_in_span is true. Defaults to
            `trace_api.get_current_span()` which is the most recent span
            generated by calling tracer.start_as_current_span

        Define the parameter K-V pair to save for the current trace instance
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def clear_params(
        self,
        should_clear_global_params: bool = False,
    ) -> None:
        """
        Clearing all existing parameters for the current trace instance.

        If this is called outside of an active trace, it will only clear the
        global params dict if `should_clear_global_params` is set to True.

        @param should_clear_global_params (bool): Whether to clear the global
        K-V pairs in addition to the current trace params. Defaults to false
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def add_rag_event_for_span(
        self,
        event_name: str,
        span: Optional[Span] = None,
        # TODO: Have better typing for JSON for input, output, event_data
        input: Any = None,
        output: Any = None,
        event_data: Optional[
            Union[dict[Any, Any], "DataclassInstance"]
        ] = None,
        should_also_save_in_span: bool = True,
        indexing_trace_id: Optional[str] = None,
        rag_flow_type: Optional[RagFlowType] = None,
        span_kind: Optional[str] = None,
    ) -> None:
        """
        See `AddRagEventInterface.add_rag_event_for_span`
        """

    @abc.abstractmethod
    def add_rag_event_for_trace(
        self,
        event_name: str,
        # TODO: Have better typing for JSON for input, output, event_data
        input: Any = None,
        output: Any = None,
        event_data: Optional[
            Union[dict[Any, Any], "DataclassInstance"]
        ] = None,
        indexing_trace_id: Optional[str] = None,
        rag_flow_type: Optional[RagFlowType] = None,
    ) -> None:
        """
        See `AddRagEventInterface.add_rag_event_for_trace`
        """

    @abc.abstractmethod
    def log(
        self,
        data: Any,
        # TODO: Accept str argument for user to save locally to a local file
        # logger: Optional[Union[Logger, str]] = None,
        logger: Optional[Logger] = None,
    ) -> None:
        """
        Pass in data to be logged into a separate logger. This is useful if you
        don't want to explicitly save data into span attributes, rag events, or
        param sets, but still want to log it anyways to look at later such as
        warnings, errors, or debugging info. These logs are saved to the
        LastMile database and can be accessed later when looking at trace data
        in the UI debugging tool.

        @param data (Any): The data to be logged. It gets converted to string
            format using the repr() function
        @param logger Optional(Union[Logger, str]): The logger to use for
            saving the data to. If it's a str, we assume it's the name of a
            filepath. You can have multiple loggers across different calls to
            save data to different places.
            If not defined, we use the default logger associated with
            the tracer and all the data from log calls get saved together.
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def log_feedback(
        self,
        feedback: str | dict[str, Any],
        trace_id: Optional[Union[str, int]] = None,
        span_id: Optional[Union[str, int]] = None,
        # TODO: Create macro for default timeout value
        timeout: int = 60,
    ) -> None:
        """
        Feedback is a string and optionally a free-form JSON serializable object that can be
        Specify a trace_id to link the feedback to a specific trace.
        Specify a span_id AND trace_id to link the feedback to a specific span.
        If neither are specified, the feedback is linked to the project.
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def log_binary_feedback(self, value: bool, trace_id: str) -> None:
        """
        Log binary feedback (positive or negative) for a specific trace.

        Binary feedback represents a user's simple sentiment or reaction to the assistant's
        response. Examples include thumbs up/down, helpful/unhelpful, or any other
        binary sentiment indicator.

        Args:
            value (bool): The binary feedback value. True for positive feedback,
                False for negative feedback.
            trace_id (str): The ID of the trace associated with the feedback.
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def log_numeric_feedback(self, value: int, trace_id: str) -> None:
        """
        Log numeric feedback for a specific trace.

        Numeric feedback represents a user's rating or score given to the assistant's
        response. It allows users to provide a more granular assessment of the response
        quality compared to binary feedback.

        Args:
            value (float): The numeric feedback value, typically in a defined range
                (e.g., 1 to 5).
            trace_id (str): The ID of the trace associated with the feedback.
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def log_categorical_feedback(
        self, value: str, categories: list[str], trace_id: str
    ) -> None:
        """
        Log categorical feedback for a specific trace.

        Categorical feedback allows users to select a category or label that best
        represents their assessment or sentiment regarding the assistant's response.
        The available categories are predefined and provided as a list.

        Args:
            value (str): The selected category or label for the feedback.
            categories (list[str]): The list of available categories or labels to
                choose from.
            trace_id (str): The ID of the trace associated with the feedback.
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def log_text_feedback(self, value: str, trace_id: str) -> None:
        """
        Log text feedback for a specific trace.

        Text feedback allows users to provide open-ended and unstructured feedback
        about the assistant's response. It can capture more detailed and specific
        comments or suggestions from the user.

        Args:
            value (str): The text feedback provided by the user.
            trace_id (str): The ID of the trace associated with the feedback.
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def store_trace_id(
        self,
        key: str,
        trace_id: int,
        span_id: Optional[int] = None,
        metadata: Optional[dict[str, Any]] = None,
        value_override: Any = None,  # TODO: restrict or remove
    ) -> None:
        """
        Store a key-value pair in remote storage. This is useful for retrieving
        a span or trace later on when performing online feedback or debugging.
        """

    @abc.abstractmethod
    def read_trace_id(
        self,
        key: str,
    ) -> tuple[str, str]:
        """
        Read a key-value pair from remote storage. This is useful for retrieving
        a span or trace later on when performing online feedback or debugging.

        Returns:
            tuple[str, str]: The trace_id and span_id associated with the key

        example:
        ```
        trace_id, span_id = tracer.read_trace_id("my_key")
        ```
        """
