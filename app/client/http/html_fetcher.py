from typing import Protocol


class HtmlFetcher(Protocol):
    async def fetch_html(self, url: str) -> str:
        ...
