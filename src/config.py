

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    yandex_client_id: str
    yandex_client_secret: str
    yandex_redirect_uri: str

    POSTGRES_DSN: str


def get_settings():
    return Settings()
