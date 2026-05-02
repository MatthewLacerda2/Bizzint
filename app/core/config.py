from functools import lru_cache
from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings
from typing import Any

class Settings(BaseSettings):
    
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "BizzInt"
    
    GEMINI_API_KEY: str
    #GOOGLE_REDIRECT_URI: str
    #SECRET_KEY: str
    
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    DATABASE_URL: str | None = None
    
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None, info: Any) -> Any:
        if isinstance(v, str) and v:
            return v
        
        # Accessing other fields from info.data (Pydantic v2)
        # Note: field_validator for DATABASE_URL should be after the other fields
        user = info.data.get("POSTGRES_USER")
        password = info.data.get("POSTGRES_PASSWORD")
        server = info.data.get("POSTGRES_SERVER")
        port = info.data.get("POSTGRES_PORT")
        db = info.data.get("POSTGRES_DB")
        
        return f"postgresql+asyncpg://{user}:{password}@{server}:{port}/{db}"

    TEST_DATABASE_URL: str | None = None  # Optional, only needed for tests
    
    model_config = ConfigDict(
        case_sensitive=True, 
        env_file=".env",
        env_file_encoding='utf-8',
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()