import asyncio
import logging
from abc import ABC, abstractmethod
from copy import deepcopy
from functools import wraps
from typing import Any, Callable, Dict, TypeVar

import httpx
from beacon.client.exceptions import ClientHTTPStatusException

T = TypeVar("T", bound=Callable[..., Any])

class HttpxClient(ABC):
    logger: logging.Logger
    timeout: float
    url: str

    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.url = base_url

    @abstractmethod
    def _headers(self) -> Dict[str, Any]:
        """Return the headers for the request."""

    @staticmethod
    def retry(retries: int = 1, delay: float = 0.0, backoff: float = 0.0, additive_timeout: float = 0.0) -> Callable[[T], T]:
        """Retry a function a number of times with exponential backoff and optional additive timeout."""
        if retries < 0:
            message = "retries must be 0 or greater"
            raise ValueError(message)
        if delay < 0:
            message = "delay must be 0 or greater"
            raise ValueError(message)
        if backoff < 1:
            message = "backoff must be 1 or greater"
            raise ValueError(message)

        def decorator(func: T) -> T:
            @wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                nonlocal delay  # Nonlocal is only necessary for 'delay' as it's modified
                last_exception: httpx.RequestError = None
                attempts = 0
                while attempts < retries:
                    new_kwargs = deepcopy(kwargs)
                    try:
                        # Adjust timeout for this attempt, if applicable
                        current_timeout = new_kwargs.get("timeout", 30.0)
                        current_timeout += additive_timeout * attempts

                        # Only update kwargs if we have a positive timeout adjustment
                        if current_timeout > 0:
                            new_kwargs["timeout"] = current_timeout

                        return await func(*args, **new_kwargs)
                    except (httpx.TimeoutException) as e:
                        last_exception = e
                        if attempts >= retries - 1:
                            break  # No more retries left
                        await asyncio.sleep(delay)
                        delay *= backoff
                        attempts += 1
                raise last_exception  # Re-raise the last exception if all retries failed
            return wrapper
        return decorator

    @retry(retries=1, delay=1.0, backoff=1.0, additive_timeout=0.0)
    async def post(self, endpoint: str, json_data: Dict[str, Any], timeout: float = 10.0) -> Dict[str, Any] | str:
        """Make a POST request to the API endpoint."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.url}/{endpoint}",
                json=json_data,
                headers=self._headers(),
                timeout=timeout,
            )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self.logger.error("Error response from API: %s", e)
            msg = f"Error response from API: {e}"
            raise ClientHTTPStatusException(msg) from e

        try:
            output_json = response.json()
            self.logger.debug("Successful response from API in json format: %s", str(output_json)[:50])
            return output_json
        except ValueError:
            self.logger.debug("Successful response from API in text format: %s", response.text[:50])
            return response.text
