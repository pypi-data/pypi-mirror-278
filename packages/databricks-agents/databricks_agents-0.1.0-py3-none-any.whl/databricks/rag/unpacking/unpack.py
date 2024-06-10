import os
import logging
from typing import Tuple, Optional
from enum import Enum
import json
from pyspark.sql.functions import udf

_logger = logging.getLogger(__name__)

try:
    from pyspark.sql import DataFrame
except ImportError:
    DataFrame = None
    _logger.warning(
        "`pyspark` not found, install with `pip install pyspark` for unpacking."
    )
else:
    from databricks.rag.unpacking.schemas import (
        ASSESSMENT_PROTO_SCHEMA,
        CHOICES_SCHEMA,
        MESSAGES_SCHEMA,
        MLFLOW_TRACE_SCHEMA_VERSION,
        RETRIEVAL_ASSESSMENT_TABLE_SCHEMA,
        TEXT_ASSESSMENT_TABLE_SCHEMA,
        TRACE_SCHEMA,
        TRACE_V2_SCHEMA,
        APP_VERSION_ID,
    )
    from pyspark.sql import functions as F
    from pyspark.sql import types as T


# Schema Version
# V1 - When mlflow_trace_schema_version is Null in the Trace Object
# V2 - When mlflow_trace_schema_version = 2 in the Trace Object
# MLFLOW_TRACE - When Info Object exists inside of the trace
# NO_TRACE - A simple catch statement which does not process the trace. Used when trace does not exist or has an incompatible version (no info, and >v2)
class TraceSchemaVersion(Enum):
    NO_TRACE = 0
    V1 = 1
    V2 = 2
    MLFLOW_TRACE = 3


def _generate_request_logs_v1(df: DataFrame) -> DataFrame:
    request_payloads = df.filter(F.expr("response:choices IS NOT NULL"))
    request_payloads = request_payloads.filter(
        F.expr(
            f"response:databricks_output.trace['{MLFLOW_TRACE_SCHEMA_VERSION}'] IS NULL"
        )
    )
    return (
        request_payloads.withColumn(
            "request",
            F.struct(
                F.col("databricks_request_id").alias("request_id"),
                F.expr("request:databricks_options.conversation_id").alias(
                    "conversation_id"
                ),
                F.col("timestamp"),
                F.from_json(F.expr("request:messages"), MESSAGES_SCHEMA).alias(
                    "messages"
                ),
                F.element_at(
                    F.from_json(F.expr("request:messages"), MESSAGES_SCHEMA), -1
                )
                .getItem("content")
                .alias("last_input"),
            ),
        )
        .withColumn(
            "trace",
            F.from_json(F.expr("response:databricks_output.trace"), TRACE_SCHEMA),
        )
        .withColumn(
            "output",
            F.struct(
                F.from_json(F.expr("response:choices"), CHOICES_SCHEMA).alias("choices")
            ),
        )
        .withColumn("schema_version", F.lit(str(TraceSchemaVersion.V1.value)))
        .select("request", "trace", "output", "schema_version")
    )


def _generate_request_logs_no_trace(df: DataFrame) -> DataFrame:
    request_payloads = df.filter(F.expr("response:databricks_output.trace IS NULL"))
    return (
        request_payloads.withColumn("trace", F.lit(None).cast("string"))
        .select("request", "trace", "response")
        .withColumn("schema_version", F.lit(str(TraceSchemaVersion.NO_TRACE.value)))
    )


def _generate_request_logs_v2(df: DataFrame) -> DataFrame:
    request_payloads = df.filter(
        F.expr(f"response:databricks_output.trace['{MLFLOW_TRACE_SCHEMA_VERSION}']==2")
    )
    return (
        request_payloads.withColumn(
            "request",
            F.struct(
                F.col("databricks_request_id").alias("request_id"),
                F.expr("request:databricks_options.conversation_id").alias(
                    "conversation_id"
                ),
                F.col("timestamp"),
                F.from_json(F.expr("request:messages"), MESSAGES_SCHEMA).alias(
                    "messages"
                ),
                F.element_at(
                    F.from_json(F.expr("request:messages"), MESSAGES_SCHEMA), -1
                )
                .getItem("content")
                .alias("last_input"),
            ),
        )
        # Get the databricks request id from the response struct to future proof with batch inference
        .withColumn("request_id", F.expr("response:id"))
        .withColumn(
            "trace",
            F.from_json(F.expr("response:databricks_output.trace"), TRACE_V2_SCHEMA),
        )
        .withColumn(
            "output",
            F.struct(
                F.from_json(F.expr("response:choices"), CHOICES_SCHEMA).alias("choices")
            ),
        )
        .withColumn(APP_VERSION_ID, F.col("trace").getItem(APP_VERSION_ID))
        .withColumn("last_request_input", F.col("request").getItem("last_input"))
        .withColumn(
            "response_output",
            F.element_at(F.col("output").getItem("choices"), 1)
            .getItem("message")
            .getItem("content"),
        )
        .withColumn("schema_version", F.lit(str(TraceSchemaVersion.V2.value)))
        .select(
            "request_id",
            "timestamp",
            APP_VERSION_ID,
            "last_request_input",
            "response_output",
            "request",
            "output",
            "trace",
            "schema_version",
        )
    )


# Support extracting last message from ChatCompletionRequest and SplitChatMessagesRequest
# If unable to parse this request, return None and do not throw
@udf("string")
def get_last_request(request_raw):
    if request_raw is None:
        return ""
    try:
        request_json = json.loads(request_raw)
        # ChatCompletionRequest
        if "messages" in request_json:
            return request_json["messages"][-1]["content"]
        # SplitChatMessagesRequest
        elif "query" in request_json:
            return request_json["query"]
    except:
        return None
    else:
        return None


# Support extracting last response from ChatCompletionResponse and StringResponse
# If unable to parse this request, return None and do not throw
@udf("string")
def get_first_response(response_raw):
    if response_raw is None:
        return ""
    try:
        response_json = json.loads(response_raw)
        # ChatCompletionResponse output
        if "choices" in response_json:
            return response_json["choices"][0]["message"]["content"]
        # String Response Output
        elif "content" in response_json:
            return response_json["content"]
    except:
        return None
    else:
        return None


def _generate_request_logs_mlflow_trace(df: DataFrame) -> DataFrame:
    request_payloads = df.filter(
        F.expr("response:databricks_output.trace.info IS NOT NULL")
    )
    return (
        request_payloads.withColumn(
            "trace",
            F.expr("response:databricks_output.trace"),
        )
        .withColumn(
            "conversation_id", F.expr("request:databricks_options.conversation_id")
        )
        .withColumnRenamed("response", "response_raw")
        .withColumnRenamed("request", "request_raw")
        .withColumn("request", get_last_request("request_raw"))
        .withColumn("response", get_first_response("response_raw"))
        .withColumn("schema_version", F.lit(str(TraceSchemaVersion.MLFLOW_TRACE.value)))
    )


def _generate_assessment_logs(payload_df: DataFrame) -> DataFrame:
    # Assessment logs have either text assessments or retrieval assessments
    assessment_payloads = payload_df.filter(
        F.expr(
            "request:dataframe_records[0].text_assessments IS NOT NULL or request:dataframe_records[0].retrieval_assessments IS NOT NULL"
        )
    )
    assessment_logs = (
        assessment_payloads.withColumn(
            "assessments",
            F.explode(
                F.from_json(
                    F.expr("request:dataframe_records"), ASSESSMENT_PROTO_SCHEMA
                )
            ),
        )
        .withColumn(
            "text_assessments",
            # Transform the list of text assessments into a list of assessment structs (with empty
            # retrieval assessments) so we can concatenate them before exploding.
            # The ordering of the structs must match exactly to concatenate them.
            F.transform(
                F.col("assessments.text_assessments"),
                lambda ta: F.struct(
                    # Transform the proto ratings map (which only has a boolean value)
                    # to the table ratings map (which has bool_value and double_value).
                    F.struct(
                        ta.step_id,
                        F.transform_values(
                            ta.ratings,
                            lambda _, rating_val: F.struct(
                                rating_val.value.alias("value"),
                                F.lit(None).cast(T.DoubleType()).alias("double_value"),
                                rating_val.rationale,
                            ),
                        ).alias("ratings"),
                        ta.free_text_comment,
                        ta.suggested_output,
                    ).alias("text_assessment"),
                    F.lit(None)
                    .cast(RETRIEVAL_ASSESSMENT_TABLE_SCHEMA)
                    .alias("retrieval_assessment"),
                ),
            ),
        )
        .withColumn(
            "retrieval_assessments",
            # Transform the list of retrieval assessments into a list of assessment structs (with empty
            # text assessments) so we can concatenate them before exploding.
            # The ordering of the structs must match exactly to concatenate them.
            F.transform(
                F.col("assessments.retrieval_assessments"),
                lambda ra: F.struct(
                    F.lit(None)
                    .cast(TEXT_ASSESSMENT_TABLE_SCHEMA)
                    .alias("text_assessment"),
                    # Transform the proto ratings map (which only has a boolean value)
                    # to the table ratings map (which has bool_value and double_value).
                    F.struct(
                        ra.position,
                        ra.step_id,
                        F.transform_values(
                            ra.ratings,
                            lambda _, rating_val: F.struct(
                                rating_val.value.alias("value"),
                                F.lit(None).cast(T.DoubleType()).alias("double_value"),
                                rating_val.rationale,
                            ),
                        ).alias("ratings"),
                        ra.free_text_comment,
                    ).alias("retrieval_assessment"),
                ),
            ),
        )
        .withColumn(
            "all_assessments",
            F.explode(
                F.concat(
                    # Coalesce with an empty array to handle cases where only one of
                    # text_assessments or retrieval_assessments were passed.
                    F.coalesce(F.col("text_assessments"), F.array()),
                    F.coalesce(F.col("retrieval_assessments"), F.array()),
                )
            ),
        )
        .select(
            "assessments.request_id",
            F.coalesce(
                F.col("all_assessments.text_assessment.step_id"),
                F.col("all_assessments.retrieval_assessment.step_id"),
            ).alias("step_id"),
            "assessments.source",
            "timestamp",
            "all_assessments.text_assessment",
            "all_assessments.retrieval_assessment",
        )
    )
    return assessment_logs


def _generate_request_logs(
    payload_df: DataFrame, trace_version: TraceSchemaVersion
) -> DataFrame:
    # Request logs do not have both text assessments and retrieval assessments
    request_payloads = payload_df.filter(
        F.expr(
            "request:dataframe_records[0].text_assessments IS NULL and request:dataframe_records[0].retrieval_assessments IS NULL"
        )
    )
    if trace_version == TraceSchemaVersion.V1:
        return _generate_request_logs_v1(request_payloads)
    elif trace_version == TraceSchemaVersion.V2:
        return _generate_request_logs_v2(request_payloads)
    elif trace_version == TraceSchemaVersion.MLFLOW_TRACE:
        return _generate_request_logs_mlflow_trace(request_payloads)
    elif trace_version == TraceSchemaVersion.NO_TRACE:
        return _generate_request_logs_no_trace(request_payloads)


# TODO: http://go/ML-40921
# Infers Trace Schema Version based on the first row of the Unity Catalog Table
# If a trace does not exist - return a No Trace
# If a trace exists
#    - If the TraceInfo Object Exists - return MLFLOW_TRACE
#    - Otherwise
#         - If the mlflow.trace_schema.version == 2 - return V2
#    - Otherwise return V1
def _get_trace_schema_version(request_response_log_row: T.Row) -> TraceSchemaVersion:
    if request_response_log_row is None:
        return TraceSchemaVersion.NO_TRACE

    first_row_json = json.loads(request_response_log_row["response"])
    if (
        "databricks_output" not in first_row_json
        or "trace" not in first_row_json["databricks_output"]
    ):
        return TraceSchemaVersion.NO_TRACE

    trace = first_row_json["databricks_output"]["trace"]

    if "info" in trace:
        return TraceSchemaVersion.MLFLOW_TRACE
    if MLFLOW_TRACE_SCHEMA_VERSION in trace and trace[MLFLOW_TRACE_SCHEMA_VERSION] == 2:
        return TraceSchemaVersion.V2

    return TraceSchemaVersion.V1


def unpack_and_split_payloads(
    payload_df: DataFrame, first_row: Optional[T.Row] = None
) -> Tuple[DataFrame, DataFrame]:
    """
    Unpacks the request and assessment payloads from the given DataFrame
    and splits them into separate request log and assessment log DataFrames.
    :param payload_df: A DataFrame containing payloads to unpack and split
    :return: A tuple containing (request logs DataFrame, assessment logs DataFrame)
    """

    payloads = payload_df.filter(
        F.col("status_code") == "200"
    ).withColumn(  # Ignore error requests
        "timestamp", (F.col("timestamp_ms") / 1000).cast("timestamp")
    )
    if first_row is None:
        first_row = payload_df.head()
    trace_schema_version = _get_trace_schema_version(first_row)
    request_logs = _generate_request_logs(payloads, trace_schema_version)
    assessment_logs = _generate_assessment_logs(payloads)

    return request_logs, assessment_logs
