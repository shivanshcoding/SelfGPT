"""
SelfGPT — AI: Embedding Manager

Abstraction for text embeddings using Sentence-Transformers.
Used by the RAG pipeline.
"""

import logging
from functools import lru_cache
from typing import List

logger = logging.getLogger(__name__)


class EmbeddingManager:
    """Lazy-loaded embedding model manager."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", device: str = "cpu"):
        self.model_name = model_name
        self.device = device
        self._model = None
        logger.info(f"EmbeddingManager configured with {model_name} on {device}")

    def _load_model(self):
        """Lazy-load the embedding model on first use."""
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name, device=self.device)
            logger.info(f"Embedding model {self.model_name} loaded on {self.device}")
        return self._model

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of texts into vectors."""
        model = self._load_model()
        embeddings = model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    def embed_single(self, text: str) -> List[float]:
        """Embed a single text string."""
        return self.embed([text])[0]


@lru_cache()
def get_embedding_manager() -> EmbeddingManager:
    """Cached singleton."""
    from config.settings import get_settings
    settings = get_settings()
    return EmbeddingManager(
        model_name=settings.embedding_model,
        device=settings.embedding_device,
    )
