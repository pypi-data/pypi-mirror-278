from typing import List, TypeVar, Union

######################################################################
# Column/field names used in mlflow EvaluationDataset DataFrames
######################################################################
DOC_URI_COL = "doc_uri"
CHUNK_CONTENT_COL = "content"
TRACE_COL = "trace"
REQUEST_ID_COL = "request_id"
REQUEST_COL = "request"
EXPECTED_RETRIEVED_CONTEXT_COL = "expected_retrieved_context"
EXPECTED_RESPONSE_COL = "expected_response"
RESPONSE_COL = "response"
RETRIEVED_CONTEXT_COL = "retrieved_context"

# Model error message column
MODEL_ERROR_MESSAGE_COL = "model_error_message"

######################################################################
# Column/field names for the output pandas DataFrame of mlflow.evaluate
######################################################################
_AGENT_PREFIX = "agent/"
TOTAL_INPUT_TOKEN_COUNT_COL = _AGENT_PREFIX + "total_input_token_count"
TOTAL_OUTPUT_TOKEN_COUNT_COL = _AGENT_PREFIX + "total_output_token_count"
TOTAL_TOKEN_COUNT_COL = _AGENT_PREFIX + "total_token_count"
LATENCY_SECONDS_COL = _AGENT_PREFIX + "latency_seconds"

_RETRIEVAL_PREFIX = "retrieval/"
GROUND_TRUTH_RETRIEVAL_METRIC_COL_PREFIX = _RETRIEVAL_PREFIX + "ground_truth/"
GROUND_TRUTH_DOCUMENT_PREFIX = "document_"
GROUND_TRUTH_DOCUMENT_RATING_COL = (
    GROUND_TRUTH_RETRIEVAL_METRIC_COL_PREFIX + GROUND_TRUTH_DOCUMENT_PREFIX + "ratings"
)
LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX = _RETRIEVAL_PREFIX + "llm_judged/"
LLM_JUDGED_RETRIEVAL_METRIC_RATING_COL_SUFFIX = "/ratings"
LLM_JUDGED_RETRIEVAL_METRIC_RATIONALE_COL_SUFFIX = "/rationales"
LLM_JUDGED_RETRIEVAL_METRIC_ERROR_MESSAGE_COL_SUFFIX = "/error_messages"

_RESPONSE_PREFIX = "response/"
LLM_JUDGED_RESPONSE_METRIC_COL_PREFIX = _RESPONSE_PREFIX + "llm_judged/"
LLM_JUDGED_RESPONSE_METRIC_RATING_COL_SUFFIX = "/rating"
LLM_JUDGED_RESPONSE_METRIC_RATIONALE_COL_SUFFIX = "/rationale"
LLM_JUDGED_RESPONSE_METRIC_ERROR_MESSAGE_COL_SUFFIX = "/error_message"

######################################################################
# Data types for the output pandas DataFrame of mlflow.evaluate
######################################################################
ASSESSMENT_RESULT_TYPE: TypeVar = TypeVar(
    "ASSESSMENT_RESULT_TYPE", bool, str, None, List[Union[bool, str, None]]
)
METRIC_RESULT_TYPE: TypeVar = TypeVar("METRIC_RESULT_TYPE", float, int, None)


######################################################################
# Helper methods to get column names for the output pandas DataFrame of mlflow.evaluate
######################################################################


def get_response_llm_rating_col_name(assessment_name: str) -> str:
    """Returns the column name for the LLM judged response metric rating"""
    return f"{LLM_JUDGED_RESPONSE_METRIC_COL_PREFIX}{assessment_name}{LLM_JUDGED_RESPONSE_METRIC_RATING_COL_SUFFIX}"


def get_response_llm_rationale_col_name(assessment_name: str) -> str:
    """Returns the column name for the LLM judged response metric rationale"""
    return f"{LLM_JUDGED_RESPONSE_METRIC_COL_PREFIX}{assessment_name}{LLM_JUDGED_RESPONSE_METRIC_RATIONALE_COL_SUFFIX}"


def get_response_llm_error_message_col_name(assessment_name: str) -> str:
    """Returns the column name for the LLM judged response metric error message"""
    return f"{LLM_JUDGED_RESPONSE_METRIC_COL_PREFIX}{assessment_name}{LLM_JUDGED_RESPONSE_METRIC_ERROR_MESSAGE_COL_SUFFIX}"


def is_response_llm_error_message_col(column_name: str) -> bool:
    """Returns True if the column name is a LLM judged response metric error message column"""
    return column_name.startswith(
        LLM_JUDGED_RESPONSE_METRIC_COL_PREFIX
    ) and column_name.endswith(LLM_JUDGED_RESPONSE_METRIC_ERROR_MESSAGE_COL_SUFFIX)


def get_retrieval_llm_rating_col_name(assessment_name: str) -> str:
    """Returns the column name for the LLM judged retrieval metric rating"""
    return f"{LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX}{assessment_name}{LLM_JUDGED_RETRIEVAL_METRIC_RATING_COL_SUFFIX}"


def get_retrieval_llm_rationale_col_name(assessment_name: str) -> str:
    """Returns the column name for the LLM judged retrieval metric rationale"""
    return f"{LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX}{assessment_name}{LLM_JUDGED_RETRIEVAL_METRIC_RATIONALE_COL_SUFFIX}"


def get_retrieval_llm_error_message_col_name(assessment_name: str) -> str:
    """Returns the column name for the LLM judged retrieval metric error message"""
    return f"{LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX}{assessment_name}{LLM_JUDGED_RETRIEVAL_METRIC_ERROR_MESSAGE_COL_SUFFIX}"


def is_retrieval_llm_error_message_col(column_name: str) -> bool:
    """Returns True if the column name is a LLM judged retrieval metric error message column"""
    return column_name.startswith(
        LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX
    ) and column_name.endswith(LLM_JUDGED_RETRIEVAL_METRIC_ERROR_MESSAGE_COL_SUFFIX)
