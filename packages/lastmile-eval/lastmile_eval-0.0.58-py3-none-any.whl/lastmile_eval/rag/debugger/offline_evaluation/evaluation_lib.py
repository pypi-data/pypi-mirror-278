"""
Really important TODOs (that affect the whole library)

* TODO(b7r6): We use the TestSet postgres table to represent both
QuerySet and ExampleSet. This is a disaster and needs fixing.

* TODO(b7r6): dont return np.nan (please grep for this)
"""

import json
import logging
import os
import re
from dataclasses import dataclass
from enum import Enum
from functools import partial
from typing import (
    Any,
    Callable,
    Generator,
    Literal,
    Mapping,
    NewType,
    Optional,
    Sequence,
    cast,
)
from random_word import RandomWords
from urllib.parse import urlencode

import lastmile_utils.lib.core.api as core_utils
import pandas as pd
import requests
import random
import result
from result import Err, Ok

import lastmile_eval.text.metrics as text_metrics
from lastmile_eval.rag.debugger.common import core
from lastmile_eval.rag.debugger.common.www_translation import (
    df_evaluation_metrics_to_records,
    to_records,
)
from lastmile_eval.rag.debugger.general_functional_utils import (
    do_list,
    exn_to_err,
    res_reduce_list_all_ok,
    unzip2,
)

from lastmile_eval.rag.debugger.tracing.lastmile_tracer import LastMileTracer
from lastmile_eval.rag.debugger.tracing import (
    get_lastmile_tracer,
)
from lastmile_eval.rag.debugger.tracing.utils import convert_int_id_to_hex_str


for name, logger in logging.root.manager.loggerDict.items():
    try:
        if not name.startswith("lastmile"):
            logger.setLevel(logging.CRITICAL)  # type: ignore
    except Exception:
        # logger could be a PlaceHolder...
        pass

logger = logging.getLogger(__name__)
logging.basicConfig(format=core_utils.LOGGER_FMT)

# TODO(jll): control all the logging
logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("filelock").setLevel(logging.CRITICAL)


DEFAULT_QUERY_SET_NAME = "Query Set"
DEFAULT_EXAMPLE_SET_NAME = "Example Set"
DEFAULT_PROJECT_NAME = None


BatchOutputsWithOTELTraceIds = NewType(
    "BatchOutputsWithOTELTraceIds",
    tuple[list[str], list[core.OTelTraceID]],
)


class TestSetTypes(Enum):
    """
    Types represented by ExampleSet in PostGres. This is useful to keep track of internally
    because we want to distinguish (and want the user to distinguish) between QuerySet and ExampleSet.

    For now, both are stored in the TestSet table.
    """

    DFEXAMPLESET = "DFExampleSet"
    DFQUERYSET = "DFQuerySet"


@dataclass(frozen=True)
class QueryFnOutputRecord:
    output: str
    otel_trace_id: core.OTelTraceID


class TracedUserQueryFn:
    def __call__(self, query: str) -> QueryFnOutputRecord: ...


class UserQueryFn:
    def __call__(self, query: str) -> QueryFnOutputRecord: ...


def make_traced_user_query_fn(
    fn: Callable[[str], str], project_name: Optional[str]
) -> TracedUserQueryFn:
    project_name = project_name or DEFAULT_PROJECT_NAME

    class UserQueryFnImpl(TracedUserQueryFn):
        def __call__(self, query: str) -> QueryFnOutputRecord:
            tracer: LastMileTracer = get_lastmile_tracer(
                "my-tracer", project_name=project_name
            )
            with tracer.start_as_current_span(
                "evaluation_library_run_query_fn"
            ) as wrapper_span:
                trace_id_raw = wrapper_span.get_span_context().trace_id
                otel_trace_id = core.OTelTraceID(
                    convert_int_id_to_hex_str(trace_id_raw)
                )

                # TODO(jll): catch exceptions, timeout here
                # (as low as possible)
                user_output = fn(query)
                return QueryFnOutputRecord(
                    output=user_output, otel_trace_id=otel_trace_id
                )

    return UserQueryFnImpl()


# User-facing Types


@dataclass(frozen=True)
class SaveOptions:
    do_save: bool = True
    example_set_name: Optional[str] = None
    evaluation_result_name: Optional[str] = None


Evaluator = Callable[
    [pd.DataFrame],
    list[float],
]

AggregatedEvaluator = Callable[
    [pd.DataFrame],
    float,
]


@dataclass
class CreateEvaluationResponse:
    evaluation_result_id: Optional[core.EvaluationResultId]
    example_set_id: Optional[core.ExampleSetID]
    success: bool
    message: str
    df_metrics_example_level: Optional[core.DFRAGQueryExampleEvaluations] = (
        None
    )
    df_metrics_aggregated: Optional[core.DFRAGQueryDatasetEvaluations] = None


@dataclass
class CreateExampleSetResponse:
    success: bool
    message: str
    id: core.ExampleSetID


@dataclass
class CreateQuerySetResponse:
    success: bool
    message: str
    id: core.QuerySetID


@dataclass
class BatchDownloadParams:
    batch_limit: int
    search: Optional[str] = None
    trace_id: Optional[core.RAGQueryTraceID] = None
    creator_id: Optional[core.CreatorID] = None
    project_id: Optional[core.ProjectID] = None
    organization_id: Optional[core.OrganizationID] = None
    start_timestamp: Optional[str] = None
    end_timestamp: Optional[str] = None
    event_name: Optional[str] = None


def _http_get(
    base_url: str, endpoint: str, headers: dict[str, str]
) -> core.Res[requests.Response]:
    url = os.path.join(base_url, "api", endpoint)

    raw = requests.get(url, headers=headers)
    if raw.status_code != 200:
        return Err(
            ValueError(
                f"LastMile website returned error:\n{raw.text[:100]}..."
            )
        )
    return Ok(raw)


@exn_to_err
def _http_post(
    base_url: str,
    endpoint: str,
    headers: dict[str, str],
    data: core_utils.JSONDict,
) -> requests.Response:
    return requests.post(
        os.path.join(base_url, "api", endpoint), headers=headers, json=data
    )


@exn_to_err
def _http_response_to_json(
    response: requests.Response,
):
    out = response.json()
    return out


def _key_lookup(
    key: str, mapping: Mapping[str, core.T_Inv]
) -> core.Res[core.T_Inv]:
    try:
        return Ok(mapping[key])
    except KeyError as e:
        # TODO(jll) return instead of printing this stuff
        # logger.error(f"Key not found: {key}, existing keys: {mapping.keys()}")
        # logger.error("\n".join(traceback.format_stack()))
        # logger.error(traceback.format_exc())
        return Err(e)


def _http_post_and_response_id_lookup(
    base_url: str,
    endpoint: str,
    headers: dict[str, str],
    data: core_utils.JSONDict,
) -> core.Res[core.ParsedHTTPResponse]:
    response = _http_post(base_url, endpoint, headers, data)

    outcome: core.Res[core.ParsedHTTPResponse] = result.do(
        Ok(
            core.ParsedHTTPResponse(
                returned_id=id_ok,
                status_code=response_ok.status_code,
                text=response_ok.text,
            )
        )
        for response_ok in response
        for response_json_ok in _http_response_to_json(response_ok)
        for id_ok in _key_lookup("id", response_json_ok).map_err(
            lambda _: ValueError(  # type: ignore[fixme]
                f"Expected 'id' in response ({base_url, endpoint}, {data}, {response_json_ok=}, {response_ok.text=})"
            )
        )
    )
    return outcome


def _auth_header(lastmile_api_token: core.APIToken):
    return {
        "Authorization": f"Bearer {lastmile_api_token}",
    }


def _get_example_set_ids_by_name(
    base_url: core.BaseURL,
    example_set_name: str,
    lastmile_api_token: core.APIToken,
) -> core.Res[list[core.ExampleSetID]]:
    endpoint_without_args = "evaluation_test_sets/list"
    params = {"name": example_set_name}
    encoded_params = urlencode(params)
    endpoint = f"{endpoint_without_args}?{encoded_params}"
    headers = _auth_header(lastmile_api_token)
    response = _http_get(base_url, endpoint, headers)

    def _parse_response(
        response: requests.Response,
    ) -> core.Res[list[core.ExampleSetID]]:
        if response.status_code != 200:
            return Err(
                ValueError(
                    f"LastMile website returned error:\n{response.text[:100]}..."
                )
            )

        if "evaluationTestSets" not in response.json():
            return Err(
                ValueError(f"Expected 'evaluationTestSets' in response.")
            )

        example_sets: list[core_utils.JSONDict] = response.json()[
            "evaluationTestSets"
        ]

        def _raw_example_set_to_id(
            raw: core_utils.JSONDict,
        ) -> core.Res[core.ExampleSetID]:
            id_raw = _key_lookup("id", raw)
            out: core.Res[core.ExampleSetID] = result.do(
                Ok(core.ExampleSetID(str(id_ok))) for id_ok in id_raw
            )
            return out

        return res_reduce_list_all_ok(
            map(_raw_example_set_to_id, example_sets)
        )

    return response.and_then(_parse_response)


def _download_example_set_by_id(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,  # "Explicit is better than implicit." - The Zen of Python
    example_set_id: Optional[core.ExampleSetID] = None,
) -> core.Res[core.DFExampleSet]:
    # api/evaluation_test_sets/list doesn't return the underlying test cases

    query_args: dict[str, str] = {}
    if example_set_id is not None:
        query_args["testSetId"] = example_set_id
    endpoint = f"evaluation_test_cases/list?{urlencode(query_args)}"

    headers = _auth_header(lastmile_api_token)
    response = _http_get(base_url, endpoint, headers)

    def _process_response(
        response: requests.Response,
    ) -> core.Res[core.DFExampleSet]:
        raw_test_cases = response.json()["evaluationTestCases"]

        def _extract_record(
            record: dict[str, Any]
        ) -> dict[str, Optional[str]]:
            return record

        df_records = (
            pd.DataFrame.from_records(  # type: ignore
                map(_extract_record, raw_test_cases)
            )
            .rename(
                columns={
                    "id": "exampleId",
                    "testSetId": "exampleSetId",
                    "testSetName": "exampleSetName",
                }
            )
            .reset_index()
        )

        if example_set_id is not None and "exampleSetId" in df_records.columns:
            df_records = df_records.query(f"exampleSetId == '{example_set_id}'")  # type: ignore[pandas]

        if len(df_records) == 0:
            return Err(
                ValueError(
                    f"No test cases found for {example_set_id=}.\n"
                    f"If you provided a example_set_id filter, "
                    "Please check whether the ID exists "
                    "and you have permission to view it.\n"
                    f"\nLastmile website returned {response.text[:100]}...."
                )
            )

        return core.df_as_df_example_set(df_records)

    return response.and_then(_process_response)


def download_example_set_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    example_set_id: Optional[core.ExampleSetID] = None,
    example_set_name: Optional[str] = None,
) -> core.Res[core.DFExampleSet]:
    def _concat(res: list[core.DFExampleSet]) -> core.Res[core.DFExampleSet]:
        df_all = pd.concat(res)  # type: ignore
        return core.df_as_df_example_set(df_all)

    def _assign_name(
        df: core.DFExampleSet, example_set_name: Optional[str]
    ) -> core.Res[core.DFExampleSet]:
        if example_set_name is None:
            example_set_name = "<unknown>"
        out = df.assign(exampleSetName=example_set_name)  # type: ignore
        return core.df_as_df_example_set(out)

    def _get_ids_allowed(
        example_set_name: Optional[str],
        example_set_id: Optional[core.ExampleSetID],
    ) -> core.Res[list[core.ExampleSetID]]:
        # Supports 3 cases (at least input is not None).
        if example_set_id is None and example_set_name is not None:
            # Just example_set_name filter given. Simply look up the IDs.
            # (No other filtering)
            return _get_example_set_ids_by_name(
                base_url, example_set_name, lastmile_api_token
            )
        elif example_set_id is not None and example_set_name is None:
            # Just example_set_id filter given. Simply return it.
            # (No other filtering)
            return Ok([example_set_id])
        elif example_set_id is not None and example_set_name is not None:
            # Both filters given. Look up the IDs by name, then intersect them
            # with the given set ID.
            ids_by_name = _get_example_set_ids_by_name(
                base_url, example_set_name, lastmile_api_token
            )
            # Intersect the ID list corresponding to the name with the given ID
            # (If the ID list was looked up successfully).
            return result.do(
                Ok(list(set(ids_by_name_ok) & set({example_set_id})))
                for ids_by_name_ok in ids_by_name
            )
        else:
            # The only not-allowed case.
            return Err(
                ValueError(
                    "Either example_set_id or example_set_name must be provided."
                )
            )

    def _download_all_example_sets_by_id(
        ids: list[core.ExampleSetID],
        lastmile_api_token: core.APIToken,
        base_url: core.BaseURL,
    ) -> list[core.Res[core.DFExampleSet]]:
        # TODO(b7r6) use do_list for this
        return [
            _download_example_set_by_id(
                base_url,
                lastmile_api_token,
                example_set_id_,
            ).and_then(
                partial(_assign_name, example_set_name=example_set_name)
            )
            for example_set_id_ in ids
        ]

    list_dfs_downloaded = result.do(
        res_reduce_list_all_ok(
            _download_all_example_sets_by_id(
                ids_allowed_ok, lastmile_api_token, base_url
            )
        )
        for ids_allowed_ok in _get_ids_allowed(
            example_set_name, example_set_id
        )
    )

    df_all = list_dfs_downloaded.and_then(_concat)

    return df_all


def _run_evaluations_helper(
    df_test_cases: core.DFExampleSet,
    evaluators_example_level: list[core.RAGQueryExampleLevelEvaluator],
    evaluators_aggregated: list[core.DatasetLevelEvaluator],
) -> core.Res[
    tuple[
        Optional[core.DFRAGQueryExampleEvaluations],
        Optional[core.DFRAGQueryDatasetEvaluations],
    ]
]:
    example_sets = set(
        core.pd_series_as_optional_str_list(df_test_cases, "exampleSetId")
    )
    if len(example_sets) > 1:
        return Err(
            ValueError(
                "Dataset-level evaluators were given, but "
                f"multiple test sets were found: {','.join(map(str, example_sets))}"
                "\nCurrently, only one test set per dataframe "
                "is supported."
            )
        )

    df_example_level = None
    df_aggregated = None

    dfs_evaluations_example_level: list[core.DFRAGQueryExampleEvaluations] = []
    for evaluator in evaluators_example_level:
        df_example_level_ = evaluator(df_test_cases)
        dfs_evaluations_example_level.append(df_example_level_)

    if len(dfs_evaluations_example_level) > 0:
        df_example_level = cast(
            core.DFRAGQueryExampleEvaluations, pd.concat(dfs_evaluations_example_level)  # type: ignore
        )

    dfs_aggregated: list[core.DFRAGQueryDatasetEvaluations] = []
    for evaluator in evaluators_aggregated:
        df_aggregated_ = evaluator(df_test_cases)

        dfs_aggregated.append(df_aggregated_)

        if len(dfs_aggregated) > 0:
            df_aggregated = cast(
                core.DFRAGQueryDatasetEvaluations, pd.concat(dfs_aggregated)  # type: ignore
            )

    return Ok((df_example_level, df_aggregated))


def _run_and_store_evaluations_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    example_set_id: core.ExampleSetID,
    evaluation_set_name: Optional[str],
    project_id: Optional[core.ProjectID],
    example_level_evaluators: list[core.RAGQueryExampleLevelEvaluator],
    aggregated_evaluators: list[core.DatasetLevelEvaluator],
) -> core.Res[CreateEvaluationResponse]:
    base_url = core.BaseURL(base_url)
    df_test_cases = _download_example_set_by_id(
        base_url,
        lastmile_api_token,
        example_set_id,
    )

    dfs_metrics = result.do(
        _run_evaluations_helper(
            df_test_cases_ok,
            example_level_evaluators,
            aggregated_evaluators,
        )
        for df_test_cases_ok in df_test_cases
    )

    def _store_results(
        dfs_metrics: tuple[
            Optional[core.DFRAGQueryExampleEvaluations],
            Optional[core.DFRAGQueryDatasetEvaluations],
        ]
    ) -> core.Res[CreateEvaluationResponse]:
        df_metrics_example_level, df_metrics_aggregated = dfs_metrics

        return _store_evaluation_set_results_helper(
            base_url,
            lastmile_api_token,
            evaluation_set_name,
            project_id,
            example_set_id,
            df_metrics_example_level=df_metrics_example_level,
            df_metrics_aggregated=df_metrics_aggregated,
        )

    return dfs_metrics.and_then(_store_results)


def _store_evaluation_set_results_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    evaluation_set_name: Optional[str],
    project_id: Optional[core.ProjectID],
    example_set_id: core.ExampleSetID,
    df_metrics_example_level: Optional[
        core.DFRAGQueryExampleEvaluations
    ] = None,
    df_metrics_aggregated: Optional[core.DFRAGQueryDatasetEvaluations] = None,
) -> core.Res[CreateEvaluationResponse]:
    """
    Upload evaluations results for persistence and analysis in UI.

    Metrics can be either trace-level or dataset-level.
    Both are optional, at least one is required.

    """
    if df_metrics_example_level is None and df_metrics_aggregated is None:
        return Err(
            ValueError(
                "At least one of example_level or aggregated must be provided"
            )
        )

    def _get_example_set_id(
        df_metrics_example_level: Optional[core.DFRAGQueryExampleEvaluations],
        df_metrics_aggregated: Optional[core.DFRAGQueryDatasetEvaluations],
        example_set_id: core.ExampleSetID,
    ) -> core.Res[core.ExampleSetID]:
        example_set_ids_example_level: set[str] = (  # type: ignore
            set(df_metrics_example_level.exampleSetId.unique())  # type: ignore
            if df_metrics_example_level is not None
            else set()
        )
        example_set_ids_aggregated: set[str] = (  # type: ignore
            set(df_metrics_aggregated.exampleSetId.unique())  # type: ignore
            if df_metrics_aggregated is not None
            else set()
        )
        all_ids_for_metrics = set(example_set_ids_example_level) | set(
            example_set_ids_aggregated
        )
        if all_ids_for_metrics <= {example_set_id}:
            return Ok(example_set_id)
        else:
            return Err(
                ValueError(
                    "Mismatched test set IDs. Please make sure your metrics dataframes correspond to one test set."
                )
            )

    example_set_id_ = _get_example_set_id(
        df_metrics_example_level, df_metrics_aggregated, example_set_id
    )

    outcome: core.Res[CreateEvaluationResponse] = result.do(
        _store_evaluations_for_example_set(
            base_url,
            lastmile_api_token,
            evaluation_set_name,
            example_set_id_ok_,
            project_id,
            df_metrics_example_level,
            df_metrics_aggregated,
        )
        for example_set_id_ok_ in example_set_id_
    )

    return outcome


def _get_random_evaluation_set_name() -> str:
    r = RandomWords()
    word_1 = r.get_random_word()
    word_2 = r.get_random_word()
    number = random.randint(100, 999)
    return f"{word_1}-{word_2}-{number}"


def _store_evaluations_for_example_set(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    evaluation_set_name: Optional[str],
    example_set_id: core.ExampleSetID,
    project_id: Optional[core.ProjectID],
    df_metrics_example_level: Optional[core.DFRAGQueryExampleEvaluations],
    df_metrics_aggregated: Optional[core.DFRAGQueryDatasetEvaluations],
) -> core.Res[CreateEvaluationResponse]:
    evaluation_result_name = (
        evaluation_set_name or _get_random_evaluation_set_name()
    )
    endpoint = "evaluation_sets/create"
    headers = _auth_header(lastmile_api_token)

    example_level_metrics = []
    aggregated_metrics = []

    if df_metrics_example_level is not None:
        df_trace = df_metrics_example_level.query(  # type: ignore[fixme]
            f"exampleSetId == '{example_set_id}'"
        )

        example_level_metrics = df_evaluation_metrics_to_records(df_trace)

    if df_metrics_aggregated is not None:
        df_dataset = df_metrics_aggregated.query(  # type: ignore[fixme]
            f"exampleSetId == '{example_set_id}'"
        )

        aggregated_metrics = df_evaluation_metrics_to_records(df_dataset)

    # TODO(b7r6) make a type-checked translation layer to/from www to convert names.
    data: dict[str, Any] = {
        "testSetId": example_set_id,
        "name": evaluation_result_name,
        "evaluationMetrics": example_level_metrics,
        "evaluationSetMetrics": aggregated_metrics,
        "projectId": project_id,
    }
    outcome: core.Res[CreateEvaluationResponse] = result.do(
        Ok(
            CreateEvaluationResponse(
                evaluation_result_id=core.EvaluationResultId(
                    response_ok.returned_id
                ),
                example_set_id=example_set_id,
                success=response_ok.status_code == 200,
                message=response_ok.text,
                df_metrics_example_level=df_metrics_example_level,
                df_metrics_aggregated=df_metrics_aggregated,
            )
        )
        for response_ok in _http_post_and_response_id_lookup(
            base_url, endpoint, headers, data
        )
    )

    return outcome


def _default_dataset_aggregators(
    example_level_evaluator: core.RAGQueryExampleLevelEvaluator,
) -> list[core.DatasetLevelEvaluator]:
    def _agg(
        df: core.DFExampleSet, stat: str
    ) -> core.DFRAGQueryDatasetEvaluations:
        trace_evals = example_level_evaluator(df)
        aggregated = (  # type: ignore
            trace_evals.groupby(["exampleSetId", "metricName"])[["value"]]  # type: ignore
            .agg(stat)
            .reset_index()
            .drop(
                columns=[
                    "ragQueryTraceId",
                ],
                errors="ignore",
            )
        )
        renamed = aggregated.assign(  # type: ignore
            metricName=lambda df: df.metricName + "_" + stat  # type: ignore
        )

        # vscode can infer more about pandas than cli pyright
        # vscode thinks cast is redundant
        # CLI needs the cast otherwise reports:
        # "Argument type is partially unknown..."
        renamed = cast(pd.DataFrame, renamed)  # type: ignore[fixme]

        return core.df_as_df_dataset_evaluations(renamed)

    return [partial(_agg, stat=stat) for stat in ["mean", "std", "count"]]


def user_provided_evaluators_to_all_typed_evaluators(
    example_level_evaluators: Optional[
        Mapping[
            str,
            Evaluator,
        ]
        | set[str]
    ],
    aggregated_evaluators: Optional[
        Mapping[
            str,
            AggregatedEvaluator,
        ]
    ],
    lastmile_api_token: core.APIToken,
) -> core.Res[
    tuple[
        list[core.RAGQueryExampleLevelEvaluator],
        list[core.DatasetLevelEvaluator],
    ]
]:
    example_level_evaluators = example_level_evaluators or {}
    aggregated_evaluators = aggregated_evaluators or {}
    if isinstance(example_level_evaluators, set):
        example_level_evaluators = get_default_evaluators_helper(
            example_level_evaluators, lastmile_api_token=lastmile_api_token
        )

    trace_evaluators_typed = [
        core.callable_as_example_level_evaluator(metric_name, evaluator)
        for metric_name, evaluator in example_level_evaluators.items()
    ]

    given_dataset_evaluators_typed = [
        core.callable_as_aggregated_evaluator(metric_name, evaluator)
        for metric_name, evaluator in aggregated_evaluators.items()
    ]

    trace_evaluators_for_missing_dataset_evaluators = [
        core.callable_as_example_level_evaluator(metric_name, evaluator)
        for metric_name, evaluator in example_level_evaluators.items()
    ]

    default_dataset_evaluators_for_missing_names = [
        _default_dataset_aggregators(trace_evaluator)
        for trace_evaluator in trace_evaluators_for_missing_dataset_evaluators
    ]

    dataset_evaluators_typed = (
        given_dataset_evaluators_typed
        + core_utils.flatten_list(default_dataset_evaluators_for_missing_names)
    )
    if len(dataset_evaluators_typed) == 0 and len(trace_evaluators_typed) == 0:
        return Err(
            ValueError(
                "No evaluators provided or inferred. Please provide at least one evaluator."
            )
        )
    return Ok((trace_evaluators_typed, dataset_evaluators_typed))


def _post_filter_rag_tracelike(
    df: core.T_RAGTracelike, params: BatchDownloadParams
) -> core.T_RAGTracelike:
    if params.trace_id is not None:
        df = df.query(f"traceId == '{params.trace_id}'")  # type: ignore[pandas]
    if params.creator_id is not None:
        df = df.query(f"creatorId == '{params.creator_id}'")  # type: ignore[pandas]
    if params.project_id is not None:
        df = df.query(f"projectId == '{params.project_id}'")  # type: ignore[pandas]
    if params.organization_id is not None:
        df = df.query(f"organizationId == '{params.organization_id}'")  # type: ignore[pandas]
    if params.event_name is not None and "eventName" in df.columns:
        df = df.query(f"eventName == '{params.event_name}'")  # type: ignore[pandas]

    start_timestamp = params.start_timestamp
    if start_timestamp is None:
        # 3 months ago
        start_timestamp = pd.Timestamp.now() - pd.DateOffset(months=3)

    df = df.query(f"createdAt >= '{start_timestamp}'")  # type: ignore
    if params.end_timestamp is not None:
        df = df.query(f"createdAt <= '{params.end_timestamp}'")  # type: ignore

    return df


def download_rag_query_traces_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    batch_download_params: BatchDownloadParams,
) -> Generator[core.Res[core.DFRAGQueryTrace], None, None]:
    should_continue = True
    cursor: Optional[str] = None
    while should_continue:
        batch = _download_rag_query_trace_batch(
            base_url,
            lastmile_api_token,
            batch_download_params.batch_limit,
            cursor,  # type: ignore[fixme]
            batch_download_params.search,
        )
        match batch:
            case Ok((df, cursor, has_more)):
                df = _post_filter_rag_tracelike(df, batch_download_params)
                cursor = cursor
                should_continue = has_more
                if len(df) == 0:
                    continue
                yield Ok(df)
            case Err(e):
                yield Err(e)


def download_rag_events_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    batch_download_params: BatchDownloadParams,
) -> Generator[core.Res[core.DFRAGEvent], None, None]:
    should_continue = True
    cursor: Optional[str] = None
    while should_continue:
        batch = _download_rag_event_batch(
            base_url,
            lastmile_api_token,
            batch_download_params.batch_limit,
            cursor,  # type: ignore[fixme]
            batch_download_params.search,
        )
        match batch:
            case Ok((df, cursor, has_more)):
                df = _post_filter_rag_tracelike(df, batch_download_params)
                cursor = cursor
                should_continue = has_more
                if len(df) == 0:
                    continue
                yield Ok(df)
            case Err(e):
                yield Err(e)


def _download_rag_tracelike_batch(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    batch_limit: int,
    endpoint_without_args: str,
    parse_http_response_fn: Callable[
        [core.Res[requests.Response]], core.Res[core.T_RAGTracelike]
    ],
    cursor: Optional[str],
    search: Optional[str] = None,
) -> core.Res[tuple[core.T_RAGTracelike, str, bool]]:
    params = {
        "search": search,
        "pageSize": batch_limit,
        "cursor": cursor,
    }
    params = {key: value for key, value in params.items() if value is not None}
    encoded_params = urlencode(params)
    endpoint = f"{endpoint_without_args}?{encoded_params}"
    headers = _auth_header(lastmile_api_token)
    raw_response = _http_get(base_url, endpoint, headers)
    response = raw_response

    df = parse_http_response_fn(response)

    def _get_cursor(response: dict[str, Any]) -> core.Res[str]:
        if "cursor" not in response:
            return Err(ValueError(f"Expected 'cursor' in response"))
        return Ok(response["cursor"])

    def _get_has_more(response: dict[str, Any]) -> core.Res[bool]:
        if "hasMore" not in response:
            return Err(ValueError(f"Expected 'hasMore' in response"))
        return Ok(response["hasMore"])

    out: core.Res[tuple[core.T_RAGTracelike, str, bool]] = result.do(
        Ok((df_ok, cursor_ok, has_more_ok))
        for df_ok in df
        for response_ok in response
        for cursor_ok in _get_cursor(response_ok.json())
        for has_more_ok in _get_has_more(response_ok.json())
    )

    return out


def _download_rag_query_trace_batch(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    batch_limit: int,
    cursor: Optional[str],
    search: Optional[str] = None,
) -> core.Res[tuple[core.DFRAGQueryTrace, str, bool]]:
    endpoint_without_args = "rag_query_traces/list"

    def _parse_http_response(
        response: core.Res[requests.Response],
    ) -> core.Res[core.DFRAGQueryTrace]:
        match response:
            case Err(e):
                return Err(e)
            case Ok(response_ok):
                if (
                    "queryTraces" not in response_ok.json()
                    or len(response_ok.json()["queryTraces"]) == 0
                ):
                    return Err(
                        ValueError(f"No query traces found. {response=}")
                    )

        df = result.do(
            core.df_as_df_rag_query_trace(
                pd.DataFrame.from_records(  # type: ignore[pandas]
                    response_ok.json()["queryTraces"]
                ).rename(columns={"id": "ragQueryTraceId"})
            )
            for response_ok in response
        )
        return df

    return _download_rag_tracelike_batch(
        base_url,
        lastmile_api_token,
        batch_limit,
        endpoint_without_args,
        _parse_http_response,
        cursor,
        search,
    )


def _download_rag_event_batch(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    batch_limit: int,
    cursor: Optional[str],
    search: Optional[str] = None,
) -> core.Res[tuple[core.DFRAGEvent, str, bool]]:
    endpoint_without_args = "rag_events/list"

    def _parse_http_response(
        response: core.Res[requests.Response],
    ) -> core.Res[core.DFRAGEvent]:
        match response:
            case Err(e):
                return Err(e)
            case Ok(response_ok):
                if (
                    "events" not in response_ok.json()
                    or len(response_ok.json()["events"]) == 0
                ):
                    return Err(
                        ValueError(f"No query traces found. {response=}")
                    )

        df = result.do(
            core.df_as_df_rag_events(
                pd.DataFrame.from_records(  # type: ignore[pandas]
                    response_ok.json()["events"]
                ).rename(columns={"id": "ragEventId"})
            )
            for response_ok in response
        )
        return df

    return _download_rag_tracelike_batch(
        base_url,
        lastmile_api_token,
        batch_limit,
        endpoint_without_args,
        _parse_http_response,
        cursor,
        search,
    )


def _create_example_set_from_queries_outputs(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    queries: Sequence[str],
    outputs_with_trace_ids: BatchOutputsWithOTELTraceIds,
    example_set_name: Optional[str],
    ground_truth: Optional[Sequence[str]] = None,
) -> core.Res[CreateExampleSetResponse]:
    outputs, otel_trace_ids = outputs_with_trace_ids
    df = core.df_as_df_minimal_example_set(
        pd.DataFrame(
            {
                "query": queries,
                "output": outputs,
                "groundTruth": ground_truth,
                "traceId": otel_trace_ids,
            }
        )
    )

    return result.do(
        _create_example_set_from_df(
            base_url,
            lastmile_api_token,
            df_ok,
            TestSetTypes.DFEXAMPLESET,
            example_set_name,
        )
        for df_ok in df
    )


def _example_set_create_res_to_query_set_create_res(
    example_set_create_res: CreateExampleSetResponse,
) -> CreateQuerySetResponse:
    return CreateQuerySetResponse(
        success=example_set_create_res.success,
        message=example_set_create_res.message,
        id=core.QuerySetID(example_set_create_res.id),
    )


def create_query_set_helper(
    base_url: core.BaseURL,
    queries: Sequence[str] | pd.DataFrame,
    lastmile_api_token: core.APIToken,
    query_set_name: Optional[str] = None,
    ground_truths: Optional[list[str]] = None,
):
    def _get_queries(
        queries: Sequence[str] | pd.DataFrame,
    ) -> core.Res[Sequence[str]]:
        if isinstance(queries, pd.DataFrame):
            queries_gt = _get_query_and_ground_truth(queries)
            return result.do(
                Ok(queries_gt_ok[0])
                #
                for queries_gt_ok in queries_gt
            )
        else:
            return Ok(queries)

    queries_ = _get_queries(queries)

    def _create_query_set_from_queries_list(
        base_url: core.BaseURL,
        lastmile_api_token: core.APIToken,
        inputs: Sequence[str],
        ground_truth: Optional[Sequence[str]],
        query_set_name: Optional[str],
    ) -> core.Res[CreateQuerySetResponse]:
        df = core.df_as_df_minimal_example_set(
            pd.DataFrame({"query": inputs, "groundTruth": ground_truth})
        )

        example_set_res = result.do(
            _create_example_set_from_df(
                base_url,
                lastmile_api_token,
                df_ok,
                TestSetTypes.DFQUERYSET,
                query_set_name,
            )
            for df_ok in df
        )

        return example_set_res.map(
            _example_set_create_res_to_query_set_create_res
        )

    outcome = result.do(
        _create_query_set_from_queries_list(
            base_url,
            lastmile_api_token,
            queries_ok_,
            ground_truths,
            query_set_name,
        )
        for queries_ok_ in queries_
    )

    return outcome


def _create_example_set_from_df(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    df: core.DFExampleSet | core.DFMinimalExampleSet,
    represents: TestSetTypes,
    example_set_name: Optional[str],
) -> core.Res[CreateExampleSetResponse]:
    default_name = {
        TestSetTypes.DFEXAMPLESET: "Example Set",
        TestSetTypes.DFQUERYSET: "Query Set",
    }[represents]
    example_set_name = example_set_name or default_name
    endpoint = "evaluation_test_sets/create"
    headers = _auth_header(lastmile_api_token)

    allowed_columns = [
        "query",
        "context",
        "fullyResolvedPrompt",
        "llmOutput",
        "output",
        "groundTruth",
        "ragQueryTraceId",
        "traceId",
    ]

    excluded_columns = cast(list[str], list(set(df.columns) - set(allowed_columns)))  # type: ignore
    if len(excluded_columns) > 0:
        logger.warning(
            f"Must drop given columns to create Example set: {excluded_columns}"
        )

    df_allowed: pd.DataFrame = df.drop(columns=excluded_columns)  # type: ignore[pandas]

    data: core_utils.JSONDict = {
        "name": example_set_name,
        "testCases": to_records(df_allowed),
    }

    outcome: core.Res[CreateExampleSetResponse] = result.do(
        Ok(
            CreateExampleSetResponse(
                success=response_ok.status_code == 200,
                message=response_ok.text,
                id=core.ExampleSetID(response_ok.returned_id),
            )
        )
        for response_ok in _http_post_and_response_id_lookup(
            base_url, endpoint, headers, data
        )
    )
    return outcome


def clean_rag_query_tracelike_df(df: pd.DataFrame) -> pd.DataFrame:
    def _unpack_all(df: pd.DataFrame) -> pd.DataFrame:
        cols_unpack = {
            "query": "query",
            "context": "context",
            "output": "llm_output",
        }

        def _unpack_value(x: Any, key: str):
            try:
                return json.loads(x)[key]
            except Exception:
                return x

        def _unpack(df: pd.DataFrame, col: str, key: str) -> pd.Series:  # type: ignore
            try:
                out = df[col].apply(partial(_unpack_value, key=key))  # type: ignore
                return out  # type: ignore
            except Exception:
                return df[col]  # type: ignore

        def _extract_frp(df: pd.DataFrame, c: str) -> pd.Series:  # type: ignore
            s = core.pd_series_as_optional_str_list(df, c)

            def _extract_frp_value(x: Any) -> str:
                try:
                    x = json.loads(x)["fully_resolved_prompt"]
                    m = re.search(r"'content': '([^']*)'", x)
                    if m:
                        return list(m.groups())[-1]
                    else:
                        return x
                except:
                    return x

            return s.apply(_extract_frp_value)  # type: ignore

        df_input_exploded = None

        def _value_to_series(x: Any) -> pd.Series | Any:  # type: ignore
            try:
                return pd.Series(x)  # type: ignore
            except Exception:
                return x

        try:
            df_input_exploded = df["input"].apply(_value_to_series)  # type: ignore
        except Exception:
            pass

        if df_input_exploded is not None:
            for c in df_input_exploded:  # type: ignore[fixme]
                if c not in df:
                    df[c] = df_input_exploded  # type: ignore[fixme]

        df = df.assign(  # type: ignore
            **{
                col: partial(_unpack, col=col, key=key)
                for col, key in cols_unpack.items()
            },
        ).drop(columns=["index", "input"], errors="ignore")

        if "fullyResolvedPrompt" in df.columns:
            df["fullyResolvedPrompt"] = _extract_frp(df, "fullyResolvedPrompt")

        return df

    try:
        return _unpack_all(df)
    except Exception:
        return df


def run_rag_query_fn_helper(
    rag_query_fn: TracedUserQueryFn,
    queries: Sequence[str] | pd.DataFrame,
) -> core.Res[BatchOutputsWithOTELTraceIds]:
    """
    Out: (outputs, rag_query_trace_ids)

    """

    def _get_seq(
        queries: Sequence[str] | pd.DataFrame,
    ) -> core.Res[list[str]]:
        if isinstance(queries, pd.DataFrame):
            col = None
            if "input" in queries.columns:
                col = "input"
            elif "query" in queries.columns:
                col = "query"

            if col is None:
                return Err(
                    ValueError(
                        "Input set must have an 'input' or 'query' column"
                    )
                )
            return Ok(queries[col].tolist())  # type: ignore[pandas]

        else:
            return Ok(list(queries))

    queries_seq = _get_seq(queries)

    def _safe_run(query: str) -> core.Res[QueryFnOutputRecord]:
        # TODO(jll): timeout
        try:
            return Ok(rag_query_fn(query))
        except Exception as e:
            return Err(e)

    def _run_and_process_output(
        query: str,
    ) -> core.Res[tuple[str, core.OTelTraceID]]:
        return _safe_run(query).map(_extract_str_values)

    def _extract_str_values(
        output: QueryFnOutputRecord,
    ) -> tuple[str, core.OTelTraceID]:
        return output.output, output.otel_trace_id

    def _run_and_process_all(
        queries: list[str],
    ) -> core.Res[BatchOutputsWithOTELTraceIds]:
        out = (
            do_list(_run_and_process_output, queries)
            .map(unzip2)
            .map(BatchOutputsWithOTELTraceIds)
        )
        return out

    return queries_seq.and_then(_run_and_process_all)


def _get_query_and_ground_truth(
    df: pd.DataFrame,
) -> core.Res[tuple[list[str], Optional[list[str]]]]:
    """Out: (queries, ground_truth)"""
    if "query" not in df.columns:
        return Err(ValueError("The input set must contain a 'query' column."))
    else:
        queries = core.pd_series_as_str_list(df, "query", fillna="None")
        ground_truth: Optional[list[str]] = None
        if "groundTruth" in df.columns:
            ground_truth = core.pd_series_as_str_list(
                df, "groundTruth", fillna="None"
            )
        return Ok((queries, ground_truth))


def _create_or_get_example_set(
    example_set_id: Optional[core.ExampleSetID],
    examples_dataframe: Optional[pd.DataFrame],
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    example_set_name: Optional[str],
) -> core.Res[str]:
    if example_set_id is not None and examples_dataframe is None:
        return Ok(example_set_id)
    elif example_set_id is None and examples_dataframe is not None:
        return result.do(
            Ok(example_set_ok.id)
            for df_example_set_ok in core.df_as_df_minimal_example_set(
                examples_dataframe
            )
            for example_set_ok in _create_example_set_from_df(
                base_url,
                lastmile_api_token,
                df_example_set_ok,
                TestSetTypes.DFEXAMPLESET,
                example_set_name,
            )
        )
    else:
        return Err(
            ValueError(
                "Exactly one of example_set_id, examples_dataframe must be provided."
            )
        )


def get_default_evaluators_helper(
    names: set[str], lastmile_api_token: core.APIToken
) -> dict[str, Evaluator]:
    def _wrap1(
        df: pd.DataFrame,
        base_metric: Callable[[Sequence[str]], Sequence[float]],
    ):
        if df[["output"]].isnull().any().any():  # type: ignore[union-attr]
            logger.warning(
                "None values found in the input data. Check your 'output' column. Coercing to string."
            )
        output = core.pd_series_as_str_list(df, "output", fillna="None")
        return list(base_metric(output))

    def _wrap2(
        df: pd.DataFrame,
        base_metric: Callable[[Sequence[str], Sequence[str]], Sequence[float]],
        reference_col: (
            Literal["groundTruth"] | Literal["input"]
        ) = "groundTruth",
    ):
        if df[["output", reference_col]].isnull().any().any():  # type: ignore[pandas]
            logger.warning(
                f"None values found in the input data. Check your 'output' and '{reference_col}' columns. Coercing to string."
            )

        output = core.pd_series_as_str_list(df, "output", fillna="None")
        ref = core.pd_series_as_str_list(df, reference_col, fillna="None")

        return list(base_metric(output, ref))

    def _wrap3(
        df: pd.DataFrame,
        base_metric: Callable[
            [Sequence[str], Sequence[str], Sequence[str]], Sequence[float]
        ],
    ):
        if df[["output", "groundTruth", "input"]].isnull().any().any():  # type: ignore[pandas]
            logger.warning(
                "None values found in the input data. Check your 'output', 'groundTruth', and 'input' columns. Coercing to string."
            )
        output = core.pd_series_as_str_list(df, "output", fillna="None")
        ground_truth = core.pd_series_as_str_list(
            df, "groundTruth", fillna="None"
        )

        query_col = "query" if "query" in df.columns else "input"
        inputs = core.pd_series_as_str_list(df, query_col, fillna="None")
        return list(base_metric(output, ground_truth, inputs))

    unary_metrics = {
        "toxicity": text_metrics.calculate_toxicity_score,
        "sentiment": text_metrics.calculate_custom_llm_metric_example_sentiment,
    }

    binary_metrics_gt = {
        "bleu": text_metrics.calculate_bleu_score,
        "rouge1": text_metrics.calculate_rouge1_score,
        # TODO(b7r6): summarization is probably not useful for RAG, remove it for now.
        # It's also not easy to fit into the (output, GT, input) framework.
        # "summarization": text_metrics.calculate_summarization_score,
        "similarity": text_metrics.calculate_custom_llm_metric_example_semantic_similarity,
        "exact_match": text_metrics.calculate_exact_match_score,
    }
    binary_metrics_input = {
        "relevance": text_metrics.calculate_relevance_score,
    }
    ternary_metrics = {
        "faithfulness": partial(
            text_metrics.calculate_faithfulness_score,
            lastmile_api_token=lastmile_api_token,
        ),
        "qa": text_metrics.calculate_qa_score,
        "human_vs_ai": text_metrics.calculate_human_vs_ai_score,
    }

    wrap_unary: dict[str, Evaluator] = {
        name: partial(_wrap1, base_metric=base_metric)
        for name, base_metric in unary_metrics.items()
    }

    wrap_binary_gt: dict[str, Evaluator] = {
        name: partial(_wrap2, base_metric=base_metric)
        for name, base_metric in binary_metrics_gt.items()
    }

    wrap_binary_input: dict[str, Evaluator] = {
        name: partial(_wrap2, base_metric=base_metric, reference_col="input")
        for name, base_metric in binary_metrics_input.items()
    }

    wrap_ternary: dict[str, Evaluator] = {
        name: partial(_wrap3, base_metric=base_metric)
        for name, base_metric in ternary_metrics.items()
    }

    all_wrappers = {
        **wrap_unary,
        **wrap_binary_gt,
        **wrap_binary_input,
        **wrap_ternary,
    }
    return {name: all_wrappers[name] for name in names}


def _convert_df_example_set_to_query_set(
    df: core.DFExampleSet,
) -> core.Res[core.DFQuerySet]:
    renamed = df.dropna(axis=1, how="all").rename(  # type: ignore[pandas]
        columns={
            "exampleId": "queryId",
            "exampleSetId": "querySetId",
            "exampleSetName": "querySetName",
        }
    )

    return core.df_as_df_query_set(renamed)


def run_and_evaluate_helper(
    base_url: core.BaseURL,
    project_id: Optional[str],
    run_query_fn: TracedUserQueryFn,
    all_typed_evaluators: tuple[
        list[core.RAGQueryExampleLevelEvaluator],
        list[core.DatasetLevelEvaluator],
    ],
    save_options: SaveOptions,
    n_trials: int,
    lastmile_api_token: core.APIToken,
    input_set_id: Optional[core.QuerySetID] = None,
    inputs: Optional[list[str]] = None,
    ground_truths: Optional[list[str]] = None,
):
    def _get_query_set_as_lists(
        query_set_id: Optional[core.QuerySetID],
        query_list: Optional[list[str]],
        ground_truth_list: Optional[list[str]],
    ) -> core.Res[tuple[list[str], Optional[list[str]]]]:
        """OUT: (query_list, ground_truth_list)"""
        if query_list is None and ground_truth_list is not None:
            return Err(
                ValueError("ground_truths given but no input queries given.")
            )

        # This conversion is deliberate. Since we're representing both
        # with example sets (which are actually test sets in the backend),
        # we can treat a query_set_id as an example_set_id for downloading purposes.
        example_set_id = (
            core.ExampleSetID(query_set_id)
            if query_set_id is not None
            else None
        )

        # Now, if query list is None, so is ground_truth_list
        if query_list is None and query_set_id is not None:
            df_query_set_downloaded = download_example_set_helper(
                core.BaseURL(base_url),
                core.APIToken(lastmile_api_token),
                example_set_id,
            )
            return df_query_set_downloaded.and_then(
                _get_query_and_ground_truth
            )

        if query_set_id is None and query_list is not None:
            return Ok((query_list, ground_truth_list))

        return Err(
            ValueError(
                "Exactly one of (input_set_id, inputs) must be provided."
            )
        )

    def _replicate_queries_gt(
        query_gt_lists: tuple[list[str], Optional[list[str]]],
        n_trials: int,
    ) -> tuple[list[str], Optional[list[str]]]:
        queries, gt = query_gt_lists
        if gt is None:
            return queries * n_trials, None
        else:
            return queries * n_trials, gt * n_trials

    query_gt_lists = _get_query_set_as_lists(
        input_set_id, inputs, ground_truths
    ).map(partial(_replicate_queries_gt, n_trials=n_trials))

    outputs = result.do(
        run_rag_query_fn_helper(run_query_fn, query_gt_lists_ok[0])
        for query_gt_lists_ok in query_gt_lists
    )

    create_example_set_result = result.do(
        _create_example_set_from_queries_outputs(
            base_url,
            lastmile_api_token,
            queries=query_gt_lists_ok[0],
            outputs_with_trace_ids=outputs_ok,
            example_set_name=save_options.example_set_name,
            ground_truth=query_gt_lists_ok[1],
        )
        for query_gt_lists_ok in query_gt_lists
        for outputs_ok in outputs
    )

    outcome = result.do(
        _run_and_store_evaluations_helper(
            base_url,
            core.APIToken(lastmile_api_token),
            core.ExampleSetID(create_example_set_result_ok.id),
            save_options.evaluation_result_name,
            core.ProjectID(project_id) if project_id is not None else None,
            all_typed_evaluators[0],
            all_typed_evaluators[1],
        )
        for create_example_set_result_ok in create_example_set_result
    )

    return outcome


def download_query_set_helper(
    base_url: core.BaseURL,
    query_set_id: Optional[core.QuerySetID],
    query_set_name: Optional[str],
    lastmile_api_token: str,
):
    example_set_id = (
        core.ExampleSetID(query_set_id) if query_set_id is not None else None
    )

    raw = download_example_set_helper(
        core.BaseURL(base_url),
        core.APIToken(lastmile_api_token),
        example_set_id,
        query_set_name,
    )

    return (
        raw.and_then(_convert_df_example_set_to_query_set)
        .map(clean_rag_query_tracelike_df)
        .unwrap_or_raise(ValueError)
    )


def create_example_set_helper(
    base_url: core.BaseURL,
    df: pd.DataFrame,
    example_set_name: Optional[str],
    ground_truths: Optional[list[str]],
    lastmile_api_token: core.APIToken,
) -> core.Res[CreateExampleSetResponse]:
    if ground_truths is not None:
        if "groundTruth" in df.columns:
            raise ValueError(
                "`ground_truth` column was given, but the groundTruth column is already present in the DataFrame."
            )
        df["groundTruth"] = ground_truths

    outcome = result.do(
        _create_example_set_from_df(
            base_url,
            lastmile_api_token,
            df_ok,
            TestSetTypes.DFEXAMPLESET,
            example_set_name,
        )
        for df_ok in core.df_as_df_minimal_example_set(df)
    )

    return outcome


def _download_or_convert_to_example_set(
    example_set_id: Optional[core.ExampleSetID],
    examples_dataframe: Optional[pd.DataFrame],
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
) -> core.Res[core.DFExampleSet]:
    if example_set_id is not None and examples_dataframe is None:
        return download_example_set_helper(
            base_url,
            lastmile_api_token,
            example_set_id,
        )
    elif example_set_id is None and examples_dataframe is not None:
        return core.df_as_df_example_set(examples_dataframe)
    else:
        return Err(
            ValueError(
                "Exactly one of example_set_id, examples_dataframe must be provided."
            )
        )


def evaluate_helper(
    base_url: core.BaseURL,
    project_id: Optional[str],
    example_set_id: Optional[core.ExampleSetID],
    examples_dataframe: Optional[pd.DataFrame],
    lastmile_api_token: core.APIToken,
    save_options: SaveOptions,
    all_typed_evaluators: tuple[
        list[core.RAGQueryExampleLevelEvaluator],
        list[core.DatasetLevelEvaluator],
    ],
) -> core.Res[CreateEvaluationResponse]:
    if save_options.do_save:
        example_set_id_ = _create_or_get_example_set(
            example_set_id,
            examples_dataframe,
            base_url,
            lastmile_api_token,
            save_options.example_set_name,
        )

        outcome = result.do(
            _run_and_store_evaluations_helper(
                base_url,
                core.APIToken(lastmile_api_token),
                core.ExampleSetID(example_set_id_ok_),
                save_options.evaluation_result_name,
                core.ProjectID(project_id) if project_id is not None else None,
                all_typed_evaluators[0],
                all_typed_evaluators[1],
            )
            for example_set_id_ok_ in example_set_id_
        )

        return outcome
    else:
        df_examples = _download_or_convert_to_example_set(
            example_set_id,
            examples_dataframe,
            base_url,
            lastmile_api_token,
        )

        dfs_metrics = result.do(
            _run_evaluations_helper(
                df_examples_ok,
                all_typed_evaluators[0],
                all_typed_evaluators[1],
            )
            for df_examples_ok in df_examples
        )

        return result.do(
            Ok(
                CreateEvaluationResponse(
                    evaluation_result_id=None,
                    example_set_id=example_set_id,
                    success=True,
                    message="Ran evaluations locally only, did not save anything.",
                    df_metrics_example_level=dfs_metrics_ok[0],
                    df_metrics_aggregated=dfs_metrics_ok[1],
                )
            )
            for dfs_metrics_ok in dfs_metrics
        )
