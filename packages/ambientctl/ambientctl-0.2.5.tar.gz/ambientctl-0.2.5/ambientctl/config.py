from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ambient_server: str = "http://localhost:7417"


settings = Settings()
