"""Methods and classes for working with configuration files."""

import dataclasses
from typing import Any, List, Mapping, Optional

import yaml

from databricks.rag_eval.config import assessment_config
from databricks.rag_eval.utils import error_utils

BUILTIN_ASSESSMENTS_KEY = "builtin_assessments"

EVALUATOR_CONFIG__METRICS_KEY = "metrics"
EVALUATOR_CONFIG__DOMAIN_INSTRUCTIONS_KEY = "domain_instructions"
EVALUATOR_CONFIG__EXAMPLES_DF_KEY = "examples_df"
ALLOWED_EVALUATOR_CONFIG_KEYS = {
    EVALUATOR_CONFIG__METRICS_KEY,
    EVALUATOR_CONFIG__DOMAIN_INSTRUCTIONS_KEY,
    EVALUATOR_CONFIG__EXAMPLES_DF_KEY,
}

EVALUATOR_CONFIG_ARGS__EXTRA_METRICS_KEY = "extra_metrics"

JSON_STR__METRICS_KEY = "metrics"
JSON_STR__DOMAIN_INSTRUCTIONS_KEY = "domain_instructions"


@dataclasses.dataclass
class EvaluationConfig:
    """Abstraction for `evaluation` config"""

    assessment_configs: List[assessment_config.AssessmentConfig] = dataclasses.field(
        default_factory=list
    )

    def __post_init__(self):
        if self.assessment_configs is None:
            self.assessment_configs = []

    @classmethod
    def _from_dict(cls, config_dict: Mapping[str, Any]):
        if BUILTIN_ASSESSMENTS_KEY not in config_dict:
            raise error_utils.ValidationError(
                f"Invalid config {config_dict}: `{BUILTIN_ASSESSMENTS_KEY}` required."
            )

        try:
            examples_df = config_dict.get(EVALUATOR_CONFIG__EXAMPLES_DF_KEY, None)
            domain_instructions = config_dict.get(
                EVALUATOR_CONFIG__DOMAIN_INSTRUCTIONS_KEY, None
            )
            builtin_assessment_configs = (
                assessment_config.create_builtin_assessment_configs(
                    config_dict.get(BUILTIN_ASSESSMENTS_KEY) or [],
                    examples_df,
                    domain_instructions,
                )
            )
        except (TypeError, KeyError, ValueError) as error:
            raise error_utils.ValidationError(
                f"Invalid config `{config_dict[BUILTIN_ASSESSMENTS_KEY]}`: {error}"
            )
        # Handle errors internally as we don't want to surface that
        # the extra metrics are handled as a "config"
        extra_metrics = config_dict.get(EVALUATOR_CONFIG_ARGS__EXTRA_METRICS_KEY, None)
        custom_metrics_configs = (
            assessment_config.create_custom_eval_metric_assessment_configs(
                extra_metrics
            )
        )
        assessment_confs = builtin_assessment_configs + custom_metrics_configs
        all_names = [
            assessment_conf.assessment_name for assessment_conf in assessment_confs
        ]
        dups = {name for name in all_names if all_names.count(name) > 1}
        if dups:
            raise error_utils.ValidationError(
                f"Invalid config `{config_dict}`: assessment names must be unique. Found duplicate assessment names: {dups}"
            )

        try:
            result = cls(
                assessment_configs=assessment_confs,
            )
        except (TypeError, KeyError, ValueError) as error:
            raise error_utils.ValidationError(
                f"Invalid config `{config_dict}`: {error}"
            )

        return result

    @classmethod
    def from_mlflow_evaluate_args(
        cls,
        evaluator_config: Optional[Mapping[str, Any]],
        extra_metrics: Optional[List[Any]] = None,
    ) -> "EvaluationConfig":
        """Reads the config from an evaluator config"""
        if evaluator_config is None:
            evaluator_config = {}

        invalid_keys = set(evaluator_config.keys()) - ALLOWED_EVALUATOR_CONFIG_KEYS
        if invalid_keys:
            raise error_utils.ValidationError(
                f"Invalid keys in evaluator config: {', '.join(invalid_keys)}. "
                f"Allowed keys: {ALLOWED_EVALUATOR_CONFIG_KEYS}"
            )

        if EVALUATOR_CONFIG__METRICS_KEY in evaluator_config:
            metrics_list = evaluator_config[EVALUATOR_CONFIG__METRICS_KEY]
            if not isinstance(metrics_list, list) or not all(
                isinstance(metric, str) for metric in metrics_list
            ):
                raise error_utils.ValidationError(
                    f"Invalid metrics: {metrics_list}. "
                    f"Must be a list of metric names."
                )
            config_dict = {BUILTIN_ASSESSMENTS_KEY: metrics_list}
        else:
            config_dict = default_config_dict()

        if EVALUATOR_CONFIG__EXAMPLES_DF_KEY in evaluator_config:
            config_dict[EVALUATOR_CONFIG__EXAMPLES_DF_KEY] = evaluator_config[
                EVALUATOR_CONFIG__EXAMPLES_DF_KEY
            ]

        if EVALUATOR_CONFIG__DOMAIN_INSTRUCTIONS_KEY in evaluator_config:
            domain_instructions = evaluator_config[
                EVALUATOR_CONFIG__DOMAIN_INSTRUCTIONS_KEY
            ]
            if not isinstance(domain_instructions, Mapping) or not all(
                isinstance(key, str) and isinstance(val, str)
                for key, val in domain_instructions.items()
            ):
                raise error_utils.ValidationError(
                    f"Invalid domain instructions: {domain_instructions}. "
                    f"Domain instructions must be a dictionary mapping assessment names to instructions."
                )
            config_dict[EVALUATOR_CONFIG__DOMAIN_INSTRUCTIONS_KEY] = evaluator_config[
                EVALUATOR_CONFIG__DOMAIN_INSTRUCTIONS_KEY
            ]

        if extra_metrics is not None:
            config_dict[EVALUATOR_CONFIG_ARGS__EXTRA_METRICS_KEY] = extra_metrics

        return cls._from_dict(config_dict)

    def to_dict(self):
        builtin_configs = [
            conf
            for conf in self.assessment_configs
            if isinstance(conf, assessment_config.BuiltinAssessmentConfig)
        ]
        metric_names = [conf.assessment_name for conf in builtin_configs]
        domain_instructions = {
            conf.assessment_name: conf.domain_instructions
            for conf in builtin_configs
            if conf.domain_instructions is not None
        }
        output_dict = {
            JSON_STR__METRICS_KEY: metric_names,
        }
        if domain_instructions:
            output_dict[JSON_STR__DOMAIN_INSTRUCTIONS_KEY] = domain_instructions

        return output_dict


def default_config() -> str:
    """Returns the default config (in YAML)"""
    return """
builtin_assessments:
  - safety
  - groundedness
  - correctness
  - relevance_to_query
  - chunk_relevance
"""


def default_config_dict() -> Mapping[str, Any]:
    """Returns the default config as a dictionary"""
    return yaml.safe_load(default_config())
