

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    yandex_client_id: str
    yandex_client_secret: str
    yandex_redirect_uri: str
    yandex_user_info: str
    yandex_authorize: str
    yandex_token: str

    POSTGRES_DSN: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str


def get_settings():
    return Settings()
