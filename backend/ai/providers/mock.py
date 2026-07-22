"""
SelfGPT — AI Provider: Mock

Echoes back messages for frontend development / testing without any
LLM running.
"""

import asyncio
import logging
from typing import AsyncGenerator, Dict, List, Optional

from .base import BaseLLMProvider

logger = logging.getLogger(__name__)

MOCK_RESPONSE = (
    "Hello! I'm a mock AI identity running in test mode. "
    "To connect a real LLM, configure your `.env` file with "
    "a valid `LLM_PROVIDER` (e.g., `ollama` or `openai_compat`)."
)


class MockProvider(BaseLLMProvider):
    """Mock provider for testing without an LLM backend."""

    def __init__(self, **kwargs):
        logger.info("MockProvider initialized — no real LLM connected")

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        **kwargs,
    ) -> Dict:
        return {
            "content": MOCK_RESPONSE,
            "model": "mock-v1",
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": len(MOCK_RESPONSE.split()),
                "total_tokens": len(MOCK_RESPONSE.split()),
            },
            "finish_reason": "stop",
        }

    async def chat_completion_stream(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        # Simulate streaming by yielding one word at a time
        for word in MOCK_RESPONSE.split():
            yield word + " "
            await asyncio.sleep(0.05)

    async def list_models(self) -> List[str]:
        return ["mock-v1"]

    async def health_check(self) -> bool:
        return True
