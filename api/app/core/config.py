from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: AnyUrl = "sqlite:///./app.db"
    ip_hash_secret: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_days: int = 7
    redis_url: str | None = None

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
