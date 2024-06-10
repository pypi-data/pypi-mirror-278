"""
NOTE: Code in this package will be deployed in the scoring server of the RAG Studio app.
It is imperative that we keep the dependencies and imports of this package to a minimum
in order to reduce the size of the model image being served by the endpoint.

Utility functions for RAG Studio that are common across workstreams (e.g., building, deployment, or evaluation).
"""

from databricks.rag.scoring.predictions import RAGCallback


__all__ = ["RAGCallback"]
