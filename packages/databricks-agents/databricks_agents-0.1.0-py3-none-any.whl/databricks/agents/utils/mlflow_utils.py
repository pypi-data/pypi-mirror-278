import mlflow
from mlflow import MlflowClient
from mlflow.utils import databricks_utils

CHAT_COMPLETIONS_REQUEST_KEYS = ["messages"]
CHAT_COMPLETIONS_RESPONSE_KEYS = ["choices"]
SPLIT_CHAT_MESSAGES_KEYS = ["query", "history"]
STRING_RESPONSE_KEYS = ["content"]
RESERVED_INPUT_KEYS = ["databricks_options", "stream"]
RESERVED_OUTPUT_KEYS = ["databricks_output", "id"]


# TODO: use `get_register_model` when `latest_versions` is fixed for UC models
def _get_latest_model_version(model_name: str) -> int:
    """
    Get the latest model version for a given model name.
    :param model_name: The name of the model.
    :return: The latest model version.
    """
    mlflow.set_registry_uri("databricks-uc")
    mlflow_client = MlflowClient()
    latest_version = 0
    for mv in mlflow_client.search_model_versions(f"name='{model_name}'"):
        version_int = int(mv.version)
        if version_int > latest_version:
            latest_version = version_int
    return latest_version


def _is_subset_of_attrs(subset, superset):
    return all(item in superset.items() for item in subset.items())


def _check_model_is_rag_compatible(model_name: str, version: int):
    """
    Load the model and check if the schema is compatible with RAG.
    """
    try:
        from mlflow.models.rag_signatures import (
            ChatCompletionRequest,
            ChatCompletionResponse,
            MultiturnChatRequest,
            StringResponse,
        )
        from mlflow.types.schema import convert_dataclass_to_schema
    except ImportError:
        # Fail closed if the RAG signatures are not available
        return False
    mlflow.set_registry_uri("databricks-uc")
    loaded_model = mlflow.pyfunc.load_model(f"models:/{model_name}/{str(version)}")
    input_schema = loaded_model.metadata.get_input_schema()

    chat_completions_request_properties = convert_dataclass_to_schema(
        ChatCompletionRequest
    ).to_dict()[0]
    split_chat_messages_properties = convert_dataclass_to_schema(
        MultiturnChatRequest
    ).to_dict()[0]
    input_properties = input_schema.to_dict()[0]

    if _is_subset_of_attrs(chat_completions_request_properties, input_properties):
        # confirm that reserved keys and split chat messages keys are not present in the input
        if any(
            key in input_properties
            for key in RESERVED_INPUT_KEYS + SPLIT_CHAT_MESSAGES_KEYS
        ):
            raise ValueError(
                "The model schema's is not compatible with RAG. The input schema must not contain "
                "the a reserved key. "
                f"Input schema: {input_schema}"
            )
    elif _is_subset_of_attrs(split_chat_messages_properties, input_properties):
        # confirm that reserved keys and chat completions request keys are not present in the input
        if any(
            key in input_properties
            for key in RESERVED_INPUT_KEYS + CHAT_COMPLETIONS_REQUEST_KEYS
        ):
            raise ValueError(
                "The model schema's is not compatible with RAG. The input schema must not contain "
                "the a reserved key. "
                f"Input schema: {input_schema}"
            )
    # check if the model has a Pyfunc ChatModel signature
    elif input_properties == {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "required": True},
                "name": {"type": "string", "required": False},
                "role": {"type": "string", "required": True},
            },
        },
        "name": "messages",
        "required": True,
    }:
        pass
    else:
        # input schema does not match any of the expected schemas
        raise ValueError(
            "The model schema's is not compatible with RAG. The input schema must be either "
            "ChatCompletionRequest or SplitChatMessagesRequest. "
            f"Input schema: {input_schema}"
        )

    output_schema = loaded_model.metadata.get_output_schema()

    chat_completions_response_properties = convert_dataclass_to_schema(
        ChatCompletionResponse
    ).to_dict()[0]
    string_response_properties = convert_dataclass_to_schema(StringResponse).to_dict()[
        0
    ]

    output_properties = output_schema.to_dict()[0]

    if _is_subset_of_attrs(chat_completions_response_properties, output_properties):
        # confirm that reserved keys and string response keys are not present in the output
        if any(
            key in output_properties
            for key in RESERVED_OUTPUT_KEYS + STRING_RESPONSE_KEYS
        ):
            raise ValueError(
                "The model schema's is not compatible with RAG. The output schema must not contain "
                "the a reserved key. "
                f"Output schema: {output_schema}"
            )
    elif _is_subset_of_attrs(string_response_properties, output_properties):
        # confirm that reserved keys and chat completions response keys are not present in the output
        if any(
            key in output_properties
            for key in RESERVED_OUTPUT_KEYS + CHAT_COMPLETIONS_RESPONSE_KEYS
        ):
            raise ValueError(
                "The model schema's is not compatible with RAG. The output schema must not contain "
                "the a reserved key. "
                f"Output schema: {output_schema}"
            )
    # check if model has legacy output schema
    # TODO: (ML-41941) switch to block these eventually
    elif output_properties == {"type": "string", "required": True}:
        pass
    # check if the model has a Pyfunc ChatModel signature
    elif output_properties == {"type": "string", "name": "id", "required": True}:
        pass
    else:
        # output schema does not match any of the expected schemas
        raise ValueError(
            "The model schema's is not compatible with RAG. The output schema must be either "
            "ChatCompletionResponse or StringResponse. "
            f"Output schema: {output_schema}"
        )


def _get_workspace_url():
    hostname = databricks_utils.get_browser_hostname()
    return f"https://{hostname}" if hostname is not None else None
