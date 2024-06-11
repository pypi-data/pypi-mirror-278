from pathlib import Path

from pydantic import PositiveInt, StrictStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )
    DEFAULT_TIMEOUT: PositiveInt = 60
    CASH_LIFETIME: PositiveInt = 1000
    CASH_SIZE: PositiveInt = 1024
    API_PREFIX: StrictStr = "/api/integra"
    BACKGROUND_REFRESH_SECONDS: PositiveInt = 60
    MAX_BACKGROUND_REFRESH_ATTEMPTS: PositiveInt = 3


SETTINGS = Settings()
