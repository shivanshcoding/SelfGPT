"""
SelfGPT — AI: Model Manager

Central abstraction for all LLM access.  Config-driven, swappable between
Ollama (default), any OpenAI-compatible API, or a mock for testing.

Usage:
    manager = get_model_manager()
    response = await manager.generate(messages, model="llama3.2")
    async for token in manager.stream(messages):
        print(token, end="")
"""

import logging
from functools import lru_cache
from typing import AsyncGenerator, Dict, List, Optional

from config.settings import get_settings
from .providers.base import BaseLLMProvider
from .providers.ollama import OllamaProvider
from .providers.openai_compat import OpenAICompatProvider
from .providers.mock import MockProvider

logger = logging.getLogger(__name__)


class ModelManager:
    """
    Config-driven model manager.  Reads LLM_PROVIDER from env and
    instantiates the right provider.  All downstream code talks to
    this manager, never directly to a provider.
    """

    def __init__(self):
        settings = get_settings()
        self.default_model = settings.llm_default_model
        self.default_vision_model = settings.llm_default_vision_model
        self.default_temperature = settings.llm_temperature
        self.default_max_tokens = settings.llm_max_tokens
        self.provider = self._create_provider(settings)

        logger.info(
            f"ModelManager ready — provider={settings.llm_provider}, "
            f"default_model={self.default_model}"
        )

    @staticmethod
    def _create_provider(settings) -> BaseLLMProvider:
        """Factory — choose provider based on LLM_PROVIDER env var."""
        provider_name = settings.llm_provider.lower()

        if provider_name == "ollama":
            return OllamaProvider(base_url=settings.llm_base_url)

        elif provider_name == "openai_compat":
            return OpenAICompatProvider(
                base_url=settings.llm_base_url,
                api_key=settings.llm_api_key,
                default_model=settings.llm_default_model,
            )

        elif provider_name == "mock":
            return MockProvider()

        else:
            logger.warning(
                f"Unknown LLM_PROVIDER '{provider_name}', falling back to mock"
            )
            return MockProvider()

    async def generate(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: float = 0.9,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        **kwargs,
    ) -> Dict:
        """Non-streaming generation."""
        return await self.provider.chat_completion(
            messages=messages,
            model=model or self.default_model,
            temperature=temperature if temperature is not None else self.default_temperature,
            max_tokens=max_tokens or self.default_max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            **kwargs,
        )

    async def stream(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: float = 0.9,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        """Streaming generation — yields tokens."""
        async for token in self.provider.chat_completion_stream(
            messages=messages,
            model=model or self.default_model,
            temperature=temperature if temperature is not None else self.default_temperature,
            max_tokens=max_tokens or self.default_max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            **kwargs,
        ):
            yield token

    async def list_models(self) -> List[str]:
        """List models available on the current provider."""
        return await self.provider.list_models()

    async def health_check(self) -> bool:
        """Check if the LLM provider is reachable."""
        return await self.provider.health_check()


@lru_cache()
def get_model_manager() -> ModelManager:
    """Cached singleton — one manager for the app lifetime."""
    return ModelManager()
