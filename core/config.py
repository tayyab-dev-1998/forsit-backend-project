from typing import Any, Dict, Optional

from dotenv import load_dotenv
from pydantic import validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_SECRET_KEY: str

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        user = values.get("POSTGRES_USER")
        password = values.get("POSTGRES_PASSWORD")
        host = values.get("POSTGRES_HOST")
        database = values.get("POSTGRES_DB")
        port = values.get("POSTGRES_PORT")

        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    class Config:
        case_sensitive = True


settings = Settings()
