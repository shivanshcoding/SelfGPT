"""
SelfGPT — AI Provider: Ollama

Default local provider. Uses Ollama's OpenAI-compatible API at /v1/*.
Supports all models installed via `ollama pull`.
"""

import logging
from typing import AsyncGenerator, Dict, List, Optional

from openai import AsyncOpenAI

from .base import BaseLLMProvider

logger = logging.getLogger(__name__)


class OllamaProvider(BaseLLMProvider):
    """Ollama provider using its OpenAI-compatible /v1 endpoint."""

    def __init__(self, base_url: str = "http://localhost:11434", **kwargs):
        # Ollama serves an OpenAI-compatible API at /v1
        self.client = AsyncOpenAI(
            base_url=f"{base_url}/v1",
            api_key="ollama",  # Ollama doesn't need a real key
        )
        self.raw_base_url = base_url
        logger.info(f"OllamaProvider initialized at {base_url}")

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
            model=model or "llama3.2",
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
            model=model or "llama3.2",
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
        """List models available in the local Ollama instance."""
        import httpx
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.raw_base_url}/api/tags")
                resp.raise_for_status()
                data = resp.json()
                return [m["name"] for m in data.get("models", [])]
        except Exception as e:
            logger.error(f"Failed to list Ollama models: {e}")
            return []

    async def health_check(self) -> bool:
        import httpx
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.raw_base_url}/api/tags")
                return resp.status_code == 200
        except Exception:
            return False
