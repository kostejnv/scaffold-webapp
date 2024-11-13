import logging
from typing import Dict, List

from beacon.client.llm.llm import LLM
from beacon.client.llm.scheme_completion import SchemeCompletion
from beacon.settings import Settings
from openai import AsyncOpenAI
from pydantic import BaseModel


class OpenAIClient(LLM, SchemeCompletion):
    """Client for the OpenAI service."""
    _async_openai_client : AsyncOpenAI
    _logger : logging.Logger
    _temperature : float

    def __init__(self, settings: Settings | None = None, temperature: float = 0.3, model: str = "gpt-4o-2024-08-06"):
        """Initialize the client."""
        self._async_openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self._logger = logging.getLogger(__name__)
        self._temperature = temperature
        self._model = model

    async def complete(self, messages: list[dict[str, str]], max_tokens: int | None = None) -> str:
        """Complete the prompt."""
        completion = await self._async_openai_client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=self._temperature,
            max_tokens=max_tokens,
        )
        answer = completion.choices[0].message.content
        if answer is None:
            msg = "No answer was generated"
            raise ValueError(msg)
        self._logger.info("Completed prompt: %s", answer[:20])
        return answer

    async def complete_scheme(self, messages: List[Dict[str, str]], schema: type[BaseModel]) -> BaseModel:
        """Complete the scheme based on the prompt."""
        completion = await self._async_openai_client.beta.chat.completions.parse(
            model=self._model,
            messages=messages,
            response_format=schema,
        )
        structured_output = completion.choices[0].message.parsed
        self._logger.info("Completed scheme: %s", str(structured_output)[:20])
        return structured_output
