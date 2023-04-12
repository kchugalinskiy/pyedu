from pydantic import BaseSettings, PostgresDsn, validator
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = "5432"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, any]) -> any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    ENABLE_GRPC: bool
    ENABLE_HTTP: bool

    CLIENT_GRPC_HOST: str
    CLIENT_GRPC_PORT: str

    GRPC_HOST: str
    GRPC_PORT: str


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
