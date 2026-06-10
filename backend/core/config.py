from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # LLM
    anthropic_api_key: str
    anthropic_model: str = "claude-3-haiku-20240307"

    # Embeddings
    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"

    # Vector store
    chroma_persist_path: str = "./chroma_data"

    # RAG
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_top_k: int = 4
    llm_temperature: float = 0.1

    # App
    environment: str = "development"
    log_level: str = "INFO"
    max_file_size_mb: int = 50
    allowed_extensions: str = "pdf,docx,txt"

    @property
    def allowed_extensions_list(self) -> list[str]:
        return [ext.strip().lower() for ext in self.allowed_extensions.split(",")]

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
