
from pydantic import BaseModel


class TestPayload(BaseModel):
    """Test payload for testing the API."""
    authorize_token: str
