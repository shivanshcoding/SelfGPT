"""
SelfGPT — AI Provider: Base Interface

Abstract interface that all LLM providers must implement.
"""

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, List, Optional


class BaseLLMProvider(ABC):
    """Abstract base for LLM providers."""

    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        top_p: float = 0.9,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        **kwargs,
    ) -> Dict:
        """
        Non-streaming chat completion.
        Returns: {"content": str, "model": str, "usage": {...}}
        """
        ...

    @abstractmethod
    async def chat_completion_stream(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        top_p: float = 0.9,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        """
        Streaming chat completion — yields tokens one at a time.
        """
        ...

    @abstractmethod
    async def list_models(self) -> List[str]:
        """List available models on this provider."""
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is reachable and ready."""
        ...
