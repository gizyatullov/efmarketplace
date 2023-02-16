import enum
from functools import lru_cache
from pathlib import Path
from tempfile import gettempdir
from typing import Optional

from dotenv import find_dotenv
from pydantic import BaseSettings
from pydantic.types import PositiveInt, SecretStr
from yarl import URL

__all__ = ['settings']

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = 'NOTSET'
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    FATAL = 'FATAL'


class _Settings(BaseSettings):
    class Config:
        """Configuration of settings."""

        #: str: env file encoding.
        env_file_encoding = 'utf-8'
        #: str: allow custom fields in model.
        arbitrary_types_allowed = True


class Settings(_Settings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = '127.0.0.1'
    API_SERVER_PORT: PositiveInt = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = 'dev'

    log_level: LogLevel = LogLevel.INFO

    #: str: Name of API service
    API_INSTANCE_APP_NAME: str
    #: PositiveInt: positive int (x > 0)
    FREQUENCY_PRICE_UPDATES_IN_MINUTES: PositiveInt = 5

    #: str: Postgresql host.
    POSTGRES_HOST: str = 'localhost'
    #: PositiveInt: positive int (x > 0) port of postgresql.
    POSTGRES_PORT: PositiveInt = 5432
    #: str: Postgresql user.
    POSTGRES_USER: str = 'postgres'
    #: SecretStr: Postgresql password.
    POSTGRES_PASSWORD: SecretStr = 'postgres'
    #: str: Postgresql database name.
    POSTGRES_DB: str = 'efmarketplace'
    db_echo: bool = False

    #: SecretStr: Key for encrypt payload in jwt.
    AUTHJWT_SECRET_KEY: str = '...'
    #: PositiveInt: Access token validity time in minutes
    ACCESS_TOKEN_EXPIRES: PositiveInt = 20
    #: PositiveInt: Refresh token validity time in days
    REFRESH_TOKEN_EXPIRES: PositiveInt = 30

    #: PositiveInt: The storage time of the uid-value captcha in redis in seconds
    CAPTCHA_TTL: PositiveInt = 3600
    #: PositiveInt: The number of characters issued in the captcha
    CAPTCHA_NUMBER_CHARACTERS: PositiveInt = 8

    #: str: Redis host
    REDIS_HOST: str = 'localhost'
    #: PositiveInt: (x > 0) port of redis
    REDIS_PORT: PositiveInt = 6379
    #: SecretStr: Redis password
    REDIS_PASSWORD: Optional[SecretStr] = None
    REDIS_BASE: Optional[PositiveInt] = None
    REDIS_USER: Optional[str] = None

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme='postgres',
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            path=f'/{self.POSTGRES_DB}',
        )

    @property
    def redis_url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.
        """
        path = ''
        if self.REDIS_BASE is not None:
            path = f'/{self.REDIS_BASE}'
        return URL.build(
            scheme='redis',
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            user=self.REDIS_USER,
            password=self.REDIS_PASSWORD,
            path=path,
        )


@lru_cache()
def get_settings(env_file: str = '.env') -> Settings:
    """Create settings instance."""
    return Settings(_env_file=find_dotenv(env_file))


settings: Settings = get_settings()
