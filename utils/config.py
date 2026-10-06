import os
from functools import lru_cache
from dotenv import load_dotenv
from pydantic import BaseModel, Field
load_dotenv()
class Settings(BaseModel):
    app_name: str = Field(default_factory=lambda: os.getenv("APP_NAME", "LegalEase"))
    app_env: str = Field(default_factory=lambda: os.getenv("APP_ENV", "development"))
    backend_url: str = Field(default_factory=lambda: os.getenv("BACKEND_URL", "http://127.0.0.1:8000"))
    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    gemini_model: str = Field(default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest"))
    demo_mode: bool = Field(default_factory=lambda: os.getenv("DEMO_MODE", "false").lower() in {"1","true","yes","on"})
    cors_origins: list[str] = Field(default_factory=lambda: [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:8501,http://127.0.0.1:8501").split(",") if x.strip()])
    request_timeout_seconds: int = Field(default_factory=lambda: int(os.getenv("REQUEST_TIMEOUT_SECONDS", "90")))
    max_document_chars: int = Field(default_factory=lambda: int(os.getenv("MAX_DOCUMENT_CHARS", "50000")))
@lru_cache
def get_settings() -> Settings:
    return Settings()
