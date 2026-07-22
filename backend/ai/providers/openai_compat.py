"""
SelfGPT — AI Provider: OpenAI-Compatible

Generic provider for any OpenAI-compatible API: Groq, Together AI,
OpenRouter, vLLM, LiteLLM, etc.  Switch by changing LLM_BASE_URL
and LLM_API_KEY in .env.
"""

import logging
from typing import AsyncGenerator, Dict, List, Optional

from openai import AsyncOpenAI

from .base import BaseLLMProvider

logger = logging.getLogger(__name__)


class OpenAICompatProvider(BaseLLMProvider):
    """Provider for any service exposing an OpenAI-compatible /v1 API."""

    def __init__(
        self,
        base_url: str,
        api_key: str = "",
        default_model: str = "gpt-3.5-turbo",
        **kwargs,
    ):
        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key or "no-key",
        )
        self.default_model = default_model
        logger.info(f"OpenAICompatProvider initialized at {base_url}")

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
        response = await self.client.chat.completions.create(
            model=model or self.default_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stream=False,
        )

        choice = response.choices[0]
        usage = response.usage

        return {
            "content": choice.message.content or "",
            "model": response.model,
            "usage": {
                "prompt_tokens": usage.prompt_tokens if usage else 0,
                "completion_tokens": usage.completion_tokens if usage else 0,
                "total_tokens": usage.total_tokens if usage else 0,
            },
            "finish_reason": choice.finish_reason,
        }

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
        stream = await self.client.chat.completions.create(
            model=model or self.default_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def list_models(self) -> List[str]:
        try:
            models = await self.client.models.list()
            return [m.id for m in models.data]
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []

    async def health_check(self) -> bool:
        try:
            await self.client.models.list()
            return True
        except Exception:
            return False
