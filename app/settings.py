from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the service."""
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
    )

    ACCESS_TOKEN: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    # Add any other settings here as needed
