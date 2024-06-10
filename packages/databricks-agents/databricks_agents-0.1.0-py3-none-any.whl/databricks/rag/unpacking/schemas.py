from pyspark.sql import types as T

######################################################################
# Constant definitions
######################################################################
APP_VERSION_ID = "app_version_id"
START_TIMESTAMP = "start_timestamp"
END_TIMESTAMP = "end_timestamp"
IS_TRUNCATED = "is_truncated"
CHUNKS = "chunks"
MLFLOW_TRACE_SCHEMA_VERSION = "mlflow.trace_schema.version"

######################################################################
# Request log schema definitions
######################################################################

# Format of the conversation following the OpenAI messages format.
MESSAGE_SCHEMA = T.StructType(
    [
        T.StructField("role", T.StringType()),
        T.StructField("content", T.StringType()),
    ]
)

# Format of the RAG response in the choices format.
CHOICES_SCHEMA = T.ArrayType(T.StructType([T.StructField("message", MESSAGE_SCHEMA)]))

# Schema of a single retrieval chunk in the trace step.
CHUNK_SCHEMA = T.StructType(
    [
        T.StructField("chunk_id", T.StringType()),
        T.StructField("doc_uri", T.StringType()),
        T.StructField("content", T.StringType()),
    ]
)

RETRIEVAL_SCHEMA = T.StructType(
    [
        T.StructField("query_text", T.StringType()),
        T.StructField(CHUNKS, T.ArrayType(CHUNK_SCHEMA)),
    ]
)

TEXT_GENERATION_SCHEMA = T.StructType(
    [
        T.StructField("prompt", T.StringType()),
        T.StructField("generated_text", T.StringType()),
    ]
)

# Schema for an individual trace step.
TRACE_STEP_SCHEMA = T.StructType(
    [
        T.StructField("step_id", T.StringType()),
        T.StructField("name", T.StringType()),
        T.StructField("type", T.StringType()),
        T.StructField(START_TIMESTAMP, T.TimestampType()),
        T.StructField(END_TIMESTAMP, T.TimestampType()),
        T.StructField("retrieval", RETRIEVAL_SCHEMA),
        T.StructField("text_generation", TEXT_GENERATION_SCHEMA),
    ]
)

# Schema of the "trace" field in the final request logs table.
TRACE_SCHEMA = T.StructType(
    [
        T.StructField(APP_VERSION_ID, T.StringType()),
        T.StructField(START_TIMESTAMP, T.TimestampType()),
        T.StructField(END_TIMESTAMP, T.TimestampType()),
        T.StructField(IS_TRUNCATED, T.BooleanType()),
        T.StructField("steps", T.ArrayType(TRACE_STEP_SCHEMA)),
    ]
)

MESSAGES_SCHEMA = T.ArrayType(MESSAGE_SCHEMA)

REQUEST_SCHEMA = T.StructType(
    [
        T.StructField("request_id", T.StringType()),
        T.StructField("conversation_id", T.StringType()),
        T.StructField("timestamp", T.TimestampType()),
        T.StructField("messages", MESSAGES_SCHEMA),
        T.StructField("last_input", T.StringType()),
    ]
)

# Full schema of the final request logs table.
REQUEST_LOG_SCHEMA = T.StructType(
    [
        T.StructField("request", REQUEST_SCHEMA),
        T.StructField("trace", TRACE_SCHEMA),
        T.StructField(
            "output",
            T.StructType([T.StructField("choices", CHOICES_SCHEMA)]),
        ),
        T.StructField("schema_version", T.StringType()),
    ]
)

######################################################################
# V2 trace schema definitions
######################################################################
SPAN_CONTEXT_SCHEMA = T.StructType(
    [
        T.StructField("span_id", T.StringType(), False),
        T.StructField("trace_id", T.StringType(), True),
    ]
)

EVENT_SCHEMA = T.StructType(
    [
        T.StructField("name", T.StringType(), False),
        T.StructField("timestamp", T.LongType(), False),
        T.StructField("attributes", T.StringType(), True),
    ]
)

SPAN_SCHEMA = T.StructType(
    [
        T.StructField("name", T.StringType(), False),
        T.StructField("context", SPAN_CONTEXT_SCHEMA, False),
        T.StructField("parent_id", T.StringType(), True),
        T.StructField("start_time", T.LongType(), False),
        T.StructField("end_time", T.LongType(), True),
        T.StructField("status_code", T.StringType(), False),
        T.StructField("status_message", T.StringType(), False),
        T.StructField("attributes", T.StringType(), True),
        T.StructField("events", T.ArrayType(EVENT_SCHEMA), True),
    ]
)

# Schema of the "trace" field in the final request logs table.
TRACE_V2_SCHEMA = T.StructType(
    [
        T.StructField(APP_VERSION_ID, T.StringType()),
        T.StructField(MLFLOW_TRACE_SCHEMA_VERSION, T.IntegerType()),
        T.StructField(START_TIMESTAMP, T.TimestampType()),
        T.StructField(END_TIMESTAMP, T.TimestampType()),
        T.StructField(IS_TRUNCATED, T.BooleanType()),
        T.StructField("spans", T.ArrayType(SPAN_SCHEMA)),
    ]
)

# Full schema of the final request logs table.
REQUEST_LOG_V2_SCHEMA = T.StructType(
    [
        T.StructField("request_id", T.StringType()),
        T.StructField("timestamp", T.TimestampType()),
        T.StructField("app_version_id", T.StringType()),
        T.StructField("last_request_input", T.StringType()),
        T.StructField("response_output", T.StringType()),
        T.StructField("request", REQUEST_SCHEMA),
        T.StructField(
            "output",
            T.StructType([T.StructField("choices", CHOICES_SCHEMA)]),
        ),
        T.StructField("trace", TRACE_V2_SCHEMA),
        T.StructField("schema_version", T.StringType()),
    ]
)

######################################################################
# Assessment log schema definitions
######################################################################

##################### Common schema definitions ######################
# Schema of the source tags in the assessment log.
ASSESSMENT_SOURCE_TAGS_SCHEMA = T.MapType(T.StringType(), T.StringType())

# Schema of the source field in the assessment log.
ASSESSMENT_SOURCE_SCHEMA = T.StructType(
    [
        T.StructField("type", T.StringType()),
        T.StructField("id", T.StringType()),
        T.StructField("tags", ASSESSMENT_SOURCE_TAGS_SCHEMA),
    ]
)

##################### Proto schema definitions #######################
# Schema of the assessments w.r.t. the proto definitions, which vary slightly from
# the final table schemas (particularly around the value of the ratings map).
RATING_VALUE_PROTO_SCHEMA = T.StructType(
    [
        T.StructField("value", T.StringType()),
        T.StructField("rationale", T.StringType()),
    ]
)

COMMON_ASSESSMENT_PROTO_SCHEMA = T.StructType(
    [
        T.StructField("step_id", T.StringType()),
        T.StructField("ratings", T.MapType(T.StringType(), RATING_VALUE_PROTO_SCHEMA)),
        T.StructField("free_text_comment", T.StringType()),
    ]
)

TEXT_ASSESSMENT_PROTO_SCHEMA = T.StructType(
    [
        *COMMON_ASSESSMENT_PROTO_SCHEMA,
        T.StructField("suggested_output", T.StringType()),
    ]
)

RETRIEVAL_ASSESSMENT_PROTO_SCHEMA = T.StructType(
    [
        T.StructField("position", T.IntegerType()),
        *COMMON_ASSESSMENT_PROTO_SCHEMA,
    ]
)

# Schema of the assessment protos from the inference table's dataframe_records.
ASSESSMENT_PROTO_SCHEMA = T.ArrayType(
    T.StructType(
        [
            T.StructField("request_id", T.StringType()),
            T.StructField("step_id", T.StringType()),
            T.StructField("source", ASSESSMENT_SOURCE_SCHEMA),
            T.StructField(
                "text_assessments", T.ArrayType(TEXT_ASSESSMENT_PROTO_SCHEMA)
            ),
            T.StructField(
                "retrieval_assessments", T.ArrayType(RETRIEVAL_ASSESSMENT_PROTO_SCHEMA)
            ),
        ]
    )
)

##################### Table schema definitions #######################
RATING_VALUE_TABLE_SCHEMA = T.StructType(
    [
        T.StructField("value", T.StringType()),
        T.StructField("double_value", T.DoubleType()),
        T.StructField("rationale", T.StringType()),
    ]
)

# Fields of the assessment structs that are common to both text and retrieval assessments.
COMMON_ASSESSMENT_TABLE_SCHEMA = [
    T.StructField("step_id", T.StringType()),
    T.StructField(
        "ratings",
        T.MapType(
            T.StringType(),
            RATING_VALUE_TABLE_SCHEMA,
        ),
    ),
    T.StructField("free_text_comment", T.StringType()),
]

# Schema of text assessments.
TEXT_ASSESSMENT_TABLE_SCHEMA = T.StructType(
    [
        *COMMON_ASSESSMENT_TABLE_SCHEMA,
        T.StructField("suggested_output", T.StringType()),
    ]
)

# Schema of retrieval assessments.
RETRIEVAL_ASSESSMENT_TABLE_SCHEMA = T.StructType(
    [
        T.StructField("position", T.IntegerType()),
        *COMMON_ASSESSMENT_TABLE_SCHEMA,
    ]
)

# Full schema of the final assessment logs table.
ASSESSMENT_LOG_SCHEMA = T.StructType(
    [
        T.StructField("request_id", T.StringType()),
        T.StructField("step_id", T.StringType()),
        T.StructField("source", ASSESSMENT_SOURCE_SCHEMA),
        T.StructField("timestamp", T.TimestampType()),
        T.StructField("text_assessment", TEXT_ASSESSMENT_TABLE_SCHEMA),
        T.StructField("retrieval_assessment", RETRIEVAL_ASSESSMENT_TABLE_SCHEMA),
    ]
)

######################################################################
# Eval dataset schema definitions
######################################################################

RETRIEVAL_OUTPUT_SCHEMA = T.StructType(
    [
        T.StructField("name", T.StringType()),
        T.StructField(CHUNKS, T.ArrayType(CHUNK_SCHEMA)),
    ]
)

GROUND_TRUTH_OUTPUT_SCHEMA = T.StructType(
    [
        T.StructField("content", T.StringType()),
    ]
)

GROUND_TRUTH_SCHEMA = T.StructType(
    [
        T.StructField("text_output", GROUND_TRUTH_OUTPUT_SCHEMA),
        T.StructField("retrieval_output", RETRIEVAL_OUTPUT_SCHEMA),
    ]
)

EVAL_DATASET_INPUT_SCHEMA = T.StructType(
    [
        T.StructField("request", REQUEST_SCHEMA),
        T.StructField("ground_truth", GROUND_TRUTH_SCHEMA),
    ]
)

EVAL_DATASET_OUTPUT_SCHEMA = T.StructType(
    [
        T.StructField("request", REQUEST_SCHEMA),
        T.StructField("trace", TRACE_SCHEMA),
        T.StructField(
            "output",
            T.StructType([T.StructField("choices", CHOICES_SCHEMA, False)]),
            False,
        ),
        T.StructField("ground_truth", GROUND_TRUTH_SCHEMA),
    ]
)
