from typing import Optional, Dict, Any

from pydantic import BaseSettings, PostgresDsn, validator


COMMAND_LOCATIONS = ["core"]


class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: str

    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_TOKEN_EXP_MINUTES: int = 1440

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    PG_DNS: Optional[PostgresDsn] = None

    SUPER_USER_EMAIL: str
    SUPER_USER_PASSWORD: str

    @validator("PG_DNS", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
