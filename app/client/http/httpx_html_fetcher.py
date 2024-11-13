import logging
from typing import ClassVar

import httpx
from beacon.client.http.html_fetcher import HtmlFetcher


class HttpxHtmlFetcher(HtmlFetcher):
    """Client for fetching HTML content using HTTPx."""
    _headers: ClassVar[dict[str, str]] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    }

    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger

    async def fetch_html(self, url: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self._headers)
        try:
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as e:
            msg = f"Error response from HtmlFetcher: {e}"
            self.logger.error(msg)
            raise Exception(msg) from e
