from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl

class Settings(BaseSettings):
    database_url: AnyUrl
    ip_hash_secret: str
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()