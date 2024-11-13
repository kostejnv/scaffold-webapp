from typing import Dict, List, Protocol


class LLM(Protocol):
    async def complete(self, messages: List[Dict[str, str]], max_tokens: int | None = None) -> str:
        ...
