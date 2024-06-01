from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    fief_domain: str
    fief_client_id: str
    fief_client_secret: str
    db_url: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()