"""Session for RAG evaluation."""

import dataclasses
import threading
import uuid
from typing import List, Optional


@dataclasses.dataclass
class Session:
    """
    RAG evaluation session.

    This class serves as the per-run storage for the current evaluation run.
    """

    session_id: str
    """The session ID for the current evaluation."""
    session_batch_size: Optional[int] = None
    """The number of questions to evaluate in the current evaluation."""

    warnings: List[str] = dataclasses.field(default_factory=list)
    """The list of warning messages raised from the execution of the current evaluation."""

    def set_session_batch_size(self, batch_size: int) -> None:
        """Sets the batch size for the current evaluation."""
        self.session_batch_size = batch_size

    def append_warning(self, message: str) -> None:
        """Appends a warning message to the session."""
        self.warnings.append(message)


# We use a thread-local storage to store the session for the current thread so that we allow multi-thread
# execution of the eval APIs.
_sessions = threading.local()
_SESSION_KEY = "rag-eval-session"


def init_session() -> None:
    """Initializes the session for the current thread."""
    session = Session(str(uuid.uuid4()))
    setattr(_sessions, _SESSION_KEY, session)


def current_session() -> Optional[Session]:
    """Gets the session for the current thread."""
    return getattr(_sessions, _SESSION_KEY, None)


def clear_session() -> None:
    """Clears the session for the current thread."""
    setattr(_sessions, _SESSION_KEY, None)
