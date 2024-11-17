from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_KEY: str = "default_key"
    EXTERNAL_SERVICE_URL: str = "http://localhost:8001"
    DEFAULT_PAGE_SIZE: int = 10

    class Config:
        env_file = "server.env"

settings = Settings()