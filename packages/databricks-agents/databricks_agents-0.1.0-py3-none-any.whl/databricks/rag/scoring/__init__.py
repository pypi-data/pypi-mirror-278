"""
NOTE: Code in this package will be deployed in the scoring server of the RAG Studio app.
It is imperative that we keep the dependencies and imports of this package to a minimum
in order to reduce the size of the model image being served by the endpoint.

Functionality for scoring/processing inputs to RAG chain endpoints.
"""

from databricks.rag.scoring.predictions import RAGCallback

__all__ = ["RAGCallback"]
