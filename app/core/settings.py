from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_env: str = Field(default='dev', alias='APP_ENV')
    log_level: str = Field(default='INFO', alias='LOG_LEVEL')

    database_url: str = Field(alias='DATABASE_URL')

    meli_base_url: str = Field(default='https://api.mercadolibre.com', alias='MELI_BASE_URL')
    meli_site_id: str = Field(default='MLB', alias='MELI_SITE_ID')
    meli_access_token: str | None = Field(default=None, alias='MELI_ACCESS_TOKEN')
    meli_app_id: str | None = Field(default=None, alias='MELI_APP_ID')
    meli_client_secret: str | None = Field(default=None, alias='MELI_CLIENT_SECRET')
    request_timeout_seconds: int = Field(default=30, alias='REQUEST_TIMEOUT_SECONDS')


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
