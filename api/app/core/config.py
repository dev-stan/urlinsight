from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: AnyUrl
    ip_hash_secret: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
