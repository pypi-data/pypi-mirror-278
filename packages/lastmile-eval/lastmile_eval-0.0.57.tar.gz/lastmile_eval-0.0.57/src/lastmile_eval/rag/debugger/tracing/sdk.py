"""
File to define the SDKs implementations that users can use in code, see example
folder for example on how it can be implemented
"""

import json
from typing import (
    Any,
    Dict,
    Optional,
)

import requests
from opentelemetry import trace as trace_api
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.trace.span import Span
from requests import Response


from ..common.utils import (
    raise_for_status,
    get_lastmile_api_token,
)
from .exporter import LastMileOTLPSpanExporter
from ..api import LastMileTracer
from .lastmile_tracer import LastMileTracer as LastMileTracerImpl
from .utils import log_all_trace_events_and_reset_trace_state
from ..common.types import RagFlowType


class _LastMileTracerProvider(TracerProvider):
    """
    Subclass of TracerProvider that defines the connection between LastMile
    Jaeger collector endpoint to the LastMileTracer
    """

    def __init__(
        self,
        lastmile_api_token: str,
        output_filepath: Optional[str] = None,
    ):
        super().__init__()

        self._already_defined_tracer_provider = False
        self._tracers: Dict[str, LastMileTracer] = {}

        # If output_filepath is defined, then save trace data to that file
        # instead of forwarding to an OpenTelemetry collector. This is useful
        # for debugging and demo purposes but not recommended for production.
        if output_filepath is not None:
            output_destination = open(output_filepath, "w", encoding="utf-8")
            exporter = ConsoleSpanExporter(out=output_destination)
        else:
            exporter = LastMileOTLPSpanExporter(
                log_rag_query_func=lambda: log_all_trace_events_and_reset_trace_state(
                    lastmile_api_token
                ),
                endpoint="https://lastmileai.dev/api/trace/create",
                headers={
                    "authorization": f"Bearer {lastmile_api_token}",
                    "Content-Type": "application/json",
                },
                # TODO: Add timeout argument and have default here
            )

        # We need to use SimpleSpanProcessor instead of BatchSpanProcessor
        # because BatchSpanProcessor does not call the exporter.export()
        # method until it is finished batching, but we need to call it at the
        # end of each span to reset the trace-level data otherwise we can
        # error.

        # The future workaround is to make all the trace-level data checks and
        # trace-data resetting occur OUTSIDE of the exporter.export() method,
        # and simply do those. Then we can have a state-level manager dict
        # where we keep track of traceId, and the state corresponding to that
        # so that when we call the callback log_rag_query_func(), it will take
        # in a trace_id arg to know which trace data to log
        span_processor = SimpleSpanProcessor(exporter)
        self.add_span_processor(span_processor)

    def get_tracer_from_name(
        self,
        token: str,
        tracer_name: str,
        project_name: Optional[str],
        global_params: Optional[dict[str, Any]],
        rag_flow_type: Optional[RagFlowType] = None,
    ) -> LastMileTracer:
        """
        Get the tracer object from the tracer_name. If the tracer object is
        already defined, then return that. Otherwise, create a new tracer
        """
        if tracer_name in self._tracers:
            return self._tracers[tracer_name]

        if not self._already_defined_tracer_provider:
            trace_api.set_tracer_provider(self)
            self._already_defined_tracer_provider = True

        tracer_implementor: trace_api.Tracer = trace_api.get_tracer(
            tracer_name
        )
        tracer = LastMileTracerImpl(
            token,
            tracer_implementor,
            tracer_name,
            project_name,
            global_params,
            rag_flow_type,
        )
        self._tracers[tracer_name] = tracer
        return tracer


def get_lastmile_tracer(
    tracer_name: str,
    lastmile_api_token: Optional[str] = None,
    project_name: Optional[str] = None,
    # TODO: Don't make params Any type
    initial_params: Optional[dict[str, Any]] = None,
    output_filepath: Optional[str] = None,
    rag_flow_type: Optional[RagFlowType] = None,
) -> LastMileTracer:
    """
    Return a tracer object that uses the OpenTelemetry SDK to instrument
    tracing in your code as well as other functionality such as logging
    the rag event data and registered parameters.

    See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer for available
    APIs and more details

    @param tracer_name str: The name of the tracer to be used.
    @param lastmile_api_token (str): Used for authentication.
        Create one from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens
    @param project_name Optional(str): The project name that will be
        associated with the trace data. This can help group traces in the UI
    @param initial_params Optional(dict[str, Any]): The K-V pairs to be
        registered and saved with ALL traces created using the returned tracer
        object. Defaults to None (empty dict).
    @param output_filepath Optional(str): By default, trace data is exported to
        an OpenTelemetry collector and saved into a hosted backend storage such
        as ElasticSearch. However if an output_filepath is defined,
        then the trace data is saved to that file instead. This is useful for
        debugging and demo purposes, but not recommened for production use.
    @param rag_flow_type Optional[RagFlowType]: The type of RAG flow that the
        tracer is being used in. If it is none, then the returned tracer can
        be used for both ingestion and query tracing.

    @return LastMileTracer: The tracer interface object to log OpenTelemetry data.
    """
    token = get_lastmile_api_token(lastmile_api_token)
    provider = _LastMileTracerProvider(token, output_filepath)
    return provider.get_tracer_from_name(
        token, tracer_name, project_name, initial_params, rag_flow_type
    )


def get_trace_data(
    trace_id: str,
    lastmile_api_token: Optional[str] = None,
    # TODO: Create macro for default timeout value
    timeout: int = 60,
    # TODO: Allow a verbose option so I don't have to keep setting SHOW_DEBUG
    # to true. If we do this, we'll also have to move print statement to logger
    # ones. This is P3 imo
) -> dict[str, Any]:  # TODO: Define eplicit typing for JSON response return
    """
    Get the raw trace and span data from the trace_id

    @param trace_id (str): The trace_id to get the trace data from. This is
        often the hexadecmial string representation of the trace_id int from
        the OpenTelemetry SDK.
        Ex: int_id = 123456789 -> hex value = 0x75BCD15 --> str = "75BCD15"
    @param lastmile_api_token (str): Used for authentication.
        Create one from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    @return dict[str, Any]: The trace data from the trace_id
    """
    token = get_lastmile_api_token(lastmile_api_token)
    lastmile_endpoint = f"https://lastmileai.dev/api/trace/read?id={trace_id}"
    response: Response = requests.get(
        lastmile_endpoint,
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
    )
    raise_for_status(
        response, f"Error fetching trace data for trace_id {trace_id}"
    )
    return response.json()


def list_ingestion_trace_events(
    take: int = 10,
    lastmile_api_token: Optional[str] = None,
    # TODO: Create macro for default timeout value
    timeout: int = 60,
    # TODO: Allow a verbose option so I don't have to keep setting SHOW_DEBUG
    # to true. If we do this, we'll also have to move print statement to logger
    # ones. This is P3 imo
) -> dict[str, Any]:  # TODO: Define eplicit typing for JSON response return
    """
    Get the list of ingestion trace events. TODO: Add more filtering options

    @param take (int): The number of trace events to take. Defaults to 10
    @param lastmile_api_token (str): Used for authentication. If not
        defined, will try to get the token from the LASTMILE_API_TOKEN
        environment variable.
        You can create a token from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    @return dict[str, Any]: The JSON response of the ingestion trace events
    """
    token = get_lastmile_api_token(lastmile_api_token)
    lastmile_endpoint = f"https://lastmileai.dev/api/rag_ingestion_traces/list?pageSize={str(take)}"
    response: Response = requests.get(
        lastmile_endpoint,
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
    )
    raise_for_status(
        response,
        "Error fetching ingestion trace events for project {self.project_name}, pageSize={take}",
    )
    return response.json()


def get_latest_ingestion_trace_id(
    lastmile_api_token: Optional[str] = None,
) -> str:
    """
    Convenience function to get the latest ingestion trace id.
    You can pass in this ID into the `add_rag_event_for_span` (as well as
    any of it's sub-type events, see `AddRagEventInterface`) or
    `add_rag_event_for_trace` methods to link a query trace with an
    ingestion trace.

    @param lastmile_api_token Optional(str): Used for authentication. If not
        defined, will try to get the token from the LASTMILE_API_TOKEN
        environment variable.
        You can create a token from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    @return str: The trace id corresponding to ingestion trace data
    """
    ingestion_traces: dict[str, Any] = list_ingestion_trace_events(
        take=1, lastmile_api_token=lastmile_api_token
    )
    # TODO: Handle errors
    ingestion_trace_id: str = ingestion_traces["ingestionTraces"][0]["traceId"]
    return ingestion_trace_id


def get_query_trace_event(
    query_trace_event_id: str,
    lastmile_api_token: Optional[str] = None,
    # TODO: Create macro for default timeout value
    timeout: int = 60,
    # TODO: Allow a verbose option so I don't have to keep setting SHOW_DEBUG
    # to true. If we do this, we'll also have to move print statement to logger
    # ones. This is P3 imo
) -> dict[str, Any]:  # TODO: Define eplicit typing for JSON response return
    """
    Get the query trace event from the query_trace_event_id

    @param query_trace_event_id (str): The ID for the table row under which
        this RAG query trace event is stored
    @param lastmile_api_token (str): Used for authentication. If not
        defined, will try to get the token from the LASTMILE_API_TOKEN
        environment variable.
        You can create a token from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    @return dict[str, Any]: The JSON response of the query trace events
    """
    token = get_lastmile_api_token(lastmile_api_token)
    lastmile_endpoint = f"https://lastmileai.dev/api/rag_query_traces/read?id={query_trace_event_id}"
    response: Response = requests.get(
        lastmile_endpoint,
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
    )
    raise_for_status(
        response,
        f"Error fetching query trace event for id {query_trace_event_id}",
    )
    return response.json()


def list_query_trace_events(
    take: int = 10,
    lastmile_api_token: Optional[str] = None,
    # TODO: Create macro for default timeout value
    timeout: int = 60,
    # TODO: Allow a verbose option so I don't have to keep setting SHOW_DEBUG
    # to true. If we do this, we'll also have to move print statement to logger
    # ones. This is P3 imo
) -> dict[str, Any]:  # TODO: Define eplicit typing for JSON response return
    """
    Get the list of query trace events. TODO: Add more filtering options

    @param take (int): The number of trace events to take. Defaults to 10
    @param lastmile_api_token (str): Used for authentication. If not
        defined, will try to get the token from the LASTMILE_API_TOKEN
        environment variable.
        You can create a token from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    @return dict[str, Any]: The JSON response of the query trace events
    """
    token = get_lastmile_api_token(lastmile_api_token)
    lastmile_endpoint = f"https://lastmileai.dev/api/rag_query_traces/list?pageSize={str(take)}"
    response: Response = requests.get(
        lastmile_endpoint,
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
    )
    raise_for_status(
        response,
        "Error fetching query trace events for project {self.project_name}, pageSize={take}",
    )
    return response.json()


## Helper functions
def export_span(span: Span) -> str:
    """
    Return a serialized representation of the span that can be used to start subspans in other places. See `Span.start_span` for more details.
    """
    span_context = span.get_span_context()
    span_context_dict = {
        "trace_id": span_context.trace_id,
        "span_id": span_context.span_id,
        "trace_flags": span_context.trace_flags,
        "trace_state": span_context.trace_state.to_header(),
        "is_remote": span_context.is_remote,
    }

    return json.dumps(span_context_dict)


def get_span_id(span: Optional[Span] = None) -> int:
    """
    Get the span ID from the provided span object.

    If no span object is provided, the span ID is retrieved from the current span.

    Args:
        span: The span object to retrieve the span ID from. Defaults to None.

    Returns:
        The span ID as an integer.
    """
    if span:
        return span.get_span_context().span_id

    current_span: Span = trace_api.get_current_span()
    return current_span.get_span_context().span_id


def get_trace_id(span: Optional[Span] = None) -> int:
    """
    Get the trace ID from the provided span object.

    If no span object is provided, the trace ID is retrieved from the current span.

    Args:
        span: The span object to retrieve the trace ID from. Defaults to None.

    Returns:
        The trace ID as an integer.
    """
    if span:
        return span.get_span_context().trace_id

    current_span: Span = trace_api.get_current_span()
    return current_span.get_span_context().trace_id
