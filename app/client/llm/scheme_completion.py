from typing import Dict, List, Protocol

from pydantic import BaseModel


class SchemeCompletion(Protocol):
    """Protocol for the LLM model that can complete a scheme."""

    async def complete_scheme(self, messages: List[Dict[str, str]], schema: type[BaseModel]) -> BaseModel:
        """Complete the scheme based on the prompt."""
        ...
