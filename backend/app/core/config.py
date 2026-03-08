from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    ollama_base_url: str = "https://ollama.com"
    ollama_local_url: str = "http://localhost:11434"
    ollama_api_key: Optional[str] = None
    ollama_model: str = "ministral-3:8b"
    embedding_model: str = "nomic-embed-text:v1.5"
    embedding_dimension: int = 768
    chunk_size: int = 512
    chunk_overlap: int = 50
    app_name: str = "Agentic RAG"
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
