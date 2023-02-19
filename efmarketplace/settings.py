import enum
from functools import lru_cache
from pathlib import Path
from tempfile import gettempdir

from dotenv import find_dotenv
from pydantic import BaseSettings
from pydantic.types import PositiveInt, SecretStr
from yarl import URL

TEMP_DIR = Path(gettempdir())
__all__ = ["settings", "Settings"]


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class _Settings(BaseSettings):
    class Config:
        """Configuration of settings."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        arbitrary_types_allowed = True


class Settings(_Settings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    # Service name.
    APP_NAME: str = ""
    # Service host.
    HOST: str = "localhost"
    # Service port.
    PORT: PositiveInt = 8000
    # Quantity of workers for uvicorn.
    WORKERS_COUNT: PositiveInt = 1
    # Enable uvicorn reloading.
    UVICORN_RELOAD: bool = True

    log_level: LogLevel = LogLevel.INFO

    # PostgreSQL host.
    POSTGRES_HOST: str
    # PostgreSQL port.
    POSTGRES_PORT: PositiveInt
    # PostgreSQL user.
    POSTGRES_USER: str
    # PostgreSQL password.
    POSTGRES_PASSWORD: SecretStr
    # PostgreSQL database name.
    POSTGRES_DATABASE_NAME: str

    # Secret key for creating and verifying tokens
    JWT_SECRET_KEY: SecretStr = "..."
    # Access token validity time in minutes
    ACCESS_TOKEN_EXPIRES: PositiveInt = 20
    # Refresh token validity time in days
    REFRESH_TOKEN_EXPIRES: PositiveInt = 30

    # The storage time of the uid-value captcha in redis in seconds
    CAPTCHA_TTL: PositiveInt = 3600
    # The number of characters issued in the captcha
    CAPTCHA_NUMBER_CHARACTERS: PositiveInt = 8

    # Redis host.
    REDIS_HOST: str = "localhost"
    # Redis port.
    REDIS_PORT: PositiveInt = 6379
    # Redis user.
    REDIS_USER: str = ""
    # Redis password.
    REDIS_PASSWORD: SecretStr = ""
    # Redis database id.
    REDIS_DATABASE_ID: PositiveInt = 1

    @property
    def db_url(self) -> URL:
        """
        Assemble PostgreSQL URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgres",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            path=f"/{self.POSTGRES_DATABASE_NAME}",
        )

    @property
    def redis_url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.
        """
        return URL.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            user=self.REDIS_USER,
            password=self.REDIS_PASSWORD.get_secret_value(),
            path=f"/{self.REDIS_DATABASE_ID}",
        )


@lru_cache()
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""
    return Settings(_env_file=find_dotenv(env_file))


settings = Settings()
