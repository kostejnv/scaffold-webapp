from typing import Any, Dict

from beacon.client.http.base import HttpxClient
from beacon.client.http.html_fetcher import HtmlFetcher
from beacon.settings import Settings


class AutoScraperClient(HttpxClient, HtmlFetcher):
    """Client for the Boilerplate Buster service."""

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize the client."""
        settings = settings or Settings()
        super().__init__(base_url=settings.AUTOSCRAPER_URL)

    def _headers(self) -> Dict[str, Any]:
        """Return the headers for the request."""
        return {
            "Content-Type": "application/json",
        }

    async def get_informative_content(self, url: str) -> str:
        """Get the informative content of a webpage."""
        try:
            json_data = {"url": url}
            response = self.post(endpoint="scrape", json_data=json_data, timeout=60.0)
            informative_content = (await response).get("plainText", "")
            self.logger.info("Got informative content for %s", url)
            return informative_content
        except Exception as e:
            msg = f"Error in {self.__class__.__name__}: {e}"
            self.logger.error(msg)
            raise Exception(msg) from e

    async def fetch_html(self, url: str) -> str:
        json_data = {"url": url}
        return await self.post(endpoint="html", json_data=json_data)
