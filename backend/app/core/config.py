"""
Configuration management for SuperQuantLab 2.0 Backend
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")

    # LLM API Configuration
    llm_api_key: str = Field(default="", alias="LLM_API_KEY")
    llm_api_base: str = Field(default="https://api.openai.com/v1", alias="LLM_API_BASE")
    llm_model: str = Field(default="gpt-4", alias="LLM_MODEL")

    # Data Configuration
    data_dir: str = Field(default="../data", alias="DATA_DIR")

    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000"], alias="CORS_ORIGINS"
    )

    class Config:
        env_file = ".env"
        case_sensitive = False
        populate_by_name = True


# Global settings instance
settings = Settings()

