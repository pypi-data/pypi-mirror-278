"""
File containing all the constants needed for the rag utils.
"""

from enum import Enum


# Mlflow experiment level tags
MLFLOW_RAG_APP_TAG = "mlflow.rag_app"
MLFLOW_RAG_APP_GLOBAL_CONFIG_TAG = "mlflow.rag_app_global_config"
MLFLOW_EVAL_DATASET_VERSION_TAG = "mlflow.eval_dataset_version_state"


# Metrics
TOXICITY_METRIC_NAME = "harmful"
FAITHFULNESS_METRIC_NAME = "faithful_to_context"
RELEVANCE_METRIC_NAME = "relevant_to_question_and_context"
ANSWER_CORRECTNESS_METRIC_NAME = "answer_correct"
PRECISION_AT_1_METRIC_NAME = "retrieval_precision_at_1"
PRECISION_AT_3_METRIC_NAME = "retrieval_precision_at_3"
PRECISION_AT_5_METRIC_NAME = "retrieval_precision_at_5"
NDCG_AT_1_METRIC_NAME = "retrieval_ndcg_at_1"
NDCG_AT_3_METRIC_NAME = "retrieval_ndcg_at_3"
NDCG_AT_5_METRIC_NAME = "retrieval_ndcg_at_5"
RECALL_AT_1_METRIC_NAME = "retrieval_recall_at_1"
RECALL_AT_3_METRIC_NAME = "retrieval_recall_at_3"
RECALL_AT_5_METRIC_NAME = "retrieval_recall_at_5"
LATENCY_METRIC_NAME = "latency"
TOKEN_COUNT_METRIC_NAME = "token_count"

# Eval dataset template
EVAL_DATASET_TEMPLATE = "eval_dataset_template"


# Enum class of pre-defined environment names
class EnvironmentName(str, Enum):
    END_USERS = "end_users"
    REVIEWERS = "reviewers"
    DEVELOPMENT = "development"


# Vector Search index column names
VS_INDEX_ID_COL = "chunk_id"
VS_INDEX_EMBEDDING_COL = "chunk_embedding"
VS_INDEX_TEXT_COL = "chunk_text"
VS_INDEX_DOC_URL_COL = "doc_uri"

# Source metadata file name
SOURCE_METADATA_FILE_NAME = "__source_metadata.json"
