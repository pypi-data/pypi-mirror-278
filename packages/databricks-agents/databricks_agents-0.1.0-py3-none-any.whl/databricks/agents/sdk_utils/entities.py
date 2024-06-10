# Entities for SDK

from dataclasses import dataclass
from enum import Enum
from typing import List


@dataclass
class Deployment:
    model_name: str
    model_version: str
    endpoint_name: str
    served_entity_name: str
    query_endpoint: str  # URI
    endpoint_url: str  # URI
    review_app_url: str  # URI


@dataclass
class Artifacts:
    # List of artifact uris of the format `runs:/<run_id>/<artifact_path>`
    artifact_uris: List[str]


@dataclass
class Instructions:
    instructions: str


class PermissionLevel(Enum):
    NO_PERMISSIONS = 1
    CAN_VIEW = 2
    CAN_QUERY = 3
    CAN_REVIEW = 4
    CAN_MANAGE = 5
