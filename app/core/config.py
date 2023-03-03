from pydantic import BaseSettings


class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: str

    class Config:
        case_sensitive = True
        env_file = ".env"
