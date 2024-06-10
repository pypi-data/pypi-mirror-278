from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

MLFLOW_TRACE_SCHEMA_VERSION = "mlflow.trace_schema.version"


class StatusCode(str, Enum):
    OK = "OK"
    ERROR = "ERROR"

    def __str__(self) -> str:
        return str(self.value)


class SpanType(str, Enum):
    """
    Default enum of span types
    """

    LLM = "LLM"
    CHAIN = "CHAIN"
    AGENT = "AGENT"
    TOOL = "TOOL"
    RETRIEVER = "RETRIEVER"
    EMBEDDING = "EMBEDDING"
    RERANKER = "RERANKER"
    PARSER = "PARSER"
    UNKNOWN = "UNKNOWN"

    def __str__(self) -> str:
        return str(self.value)


def _dump_dictionary(d: Optional[Dict[str, Any]]) -> Optional[str]:
    if d is None:
        return None
    # dump the whole dictionary to string for easier loading
    return json.dumps(d, cls=CustomEncoder)


@dataclass
class Span:
    """
    Span object.
    """

    name: str
    context: SpanContext
    parent_id: Optional[str] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    status_code: StatusCode = StatusCode.OK
    status_message: str = ""
    attributes: Optional[Dict[str, Any]] = None
    events: Optional[List[Event]] = None

    def json(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "context": asdict(self.context),
            "parent_id": self.parent_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status_code": str(self.status_code),
            "status_message": self.status_message,
            "attributes": _dump_dictionary(self.attributes),
            "events": (
                [event.json() for event in self.events] if self.events else None
            ),
        }


@dataclass
class SpanContext:
    span_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = ""


@dataclass
class Event:
    name: str
    timestamp: int
    attributes: Optional[Dict[str, Any]] = None

    def json(self):
        return {
            "name": self.name,
            "timestamp": self.timestamp,
            "attributes": _dump_dictionary(self.attributes),
        }


class CustomEncoder(json.JSONEncoder):
    """
    Custom encoder to handle json serialization.
    """

    def default(self, o):
        # convert datetime to string format by default
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, uuid.UUID):
            return str(o)
        try:
            return super().default(o)
        # convert object direct to string to avoid error in serialization
        except TypeError:
            return str(o)
