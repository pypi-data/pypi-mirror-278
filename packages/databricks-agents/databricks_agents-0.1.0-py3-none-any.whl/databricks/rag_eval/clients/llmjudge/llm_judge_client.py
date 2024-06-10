from typing import Dict, List, Optional

import requests
from requests import HTTPError
from urllib3.util import retry

from databricks import version
from databricks.rag_eval import env_vars, session
from databricks.rag_eval.clients.databricks_api_client import DatabricksAPIClient
from databricks.rag_eval.clients.llmjudge import proto_serde
from databricks.rag_eval.config import assessment_config, example_config
from databricks.rag_eval.config.assessment_config import (
    AssessmentType,
)
from databricks.rag_eval.evaluation import entities

SESSION_ID_HEADER = "eval-session-id"
BATCH_SIZE_HEADER = "eval-session-batch-size"
CLIENT_VERSION_HEADER = "eval-session-client-version"


class LlmJudgeClient(DatabricksAPIClient):
    """
    Client to interact with the LLM judge service (/chat-assessments).

    Note: this client reads the session from the current thread and uses it to construct the request headers.
      Make sure to construct this client in the same thread where the session is initialized.
    """

    def __init__(
        self,
        api_url: str,
        api_token: str,
    ):
        super().__init__(
            api_url=api_url,
            api_token=api_token,
            version="2.0",
        )
        self.extra_headers = self._construct_request_headers_from_session(
            session.current_session()
        )
        self.proto_serde = proto_serde.ChatAssessmentProtoSerde()

    def _request_post(
        self, retry_config: Optional[retry.Retry], url: str, json: Dict[str, str]
    ):
        with self.get_request_session(retry_config) as request_session:
            request_session.headers.update(self.extra_headers)
            return request_session.post(
                self.get_method_url(url),
                json=json,
                auth=self.get_auth(),
                headers=self.extra_headers,
            )

    def get_assessment(
        self,
        eval_item: entities.EvalItem,
        assessment_name: str,
        assessment_type: AssessmentType,
        examples: List[example_config.AssessmentExample],
        domain_instructions: Optional[str],
    ) -> List[entities.AssessmentResult]:
        """
        Retrieves the assessment results from the LLM judge service for the given eval item and requested assessment
        """
        request_json = self.proto_serde.construct_assessment_request_json(
            eval_item, assessment_name, examples, domain_instructions
        )

        retries = retry.Retry(
            total=env_vars.RAG_EVAL_LLM_JUDGE_MAX_RETRIES.get(),
            backoff_factor=env_vars.RAG_EVAL_LLM_JUDGE_BACKOFF_FACTOR.get(),
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_jitter=env_vars.RAG_EVAL_LLM_JUDGE_BACKOFF_JITTER.get(),
            allowed_methods=frozenset(
                ["GET", "POST"]
            ),  # by default, it doesn't retry on POST
        )
        resp = self._request_post(retries, "/agents/chat-assessments", request_json)

        if resp.status_code == requests.codes.ok:
            return self.proto_serde.construct_assessment_result(
                resp.json(), assessment_name
            )
        else:
            try:
                resp.raise_for_status()
            except HTTPError as e:
                return self.proto_serde.construct_assessment_error_result(
                    assessment_name,
                    assessment_type,
                    resp.status_code,
                    e,
                )

    def emit_chat_assessment_usage_event(
        self, custom_assessment: assessment_config.EvaluationMetricAssessmentConfig
    ):
        request_json = (
            self.proto_serde.construct_chat_assessment_usage_event_request_json(
                custom_assessment
            )
        )
        # Use default retries. Don't need to use response
        self._request_post(
            retry_config=None,
            url="/agents/chat-assessment-usage-events",
            json=request_json,
        )

    @classmethod
    def _construct_request_headers_from_session(
        cls, eval_session: Optional[session.Session]
    ) -> Dict[str, str]:
        """Constructs the request headers from the session."""
        headers = {CLIENT_VERSION_HEADER: version.VERSION}

        if eval_session is None:
            return headers
        headers[SESSION_ID_HEADER] = eval_session.session_id
        if eval_session.session_batch_size is not None:
            headers[BATCH_SIZE_HEADER] = str(eval_session.session_batch_size)

        return headers
