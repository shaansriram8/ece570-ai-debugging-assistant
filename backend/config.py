"""Configuration management for the AI Debugging Assistant backend."""
import os
from typing import List, Dict, Any
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Hugging Face API
    hf_api_key: str = os.getenv("HF_API_KEY", "")
    hf_api_base: str = "https://api-inference.huggingface.co/models"
    
    # Model configuration
    # NOTE: Update these to match your actual Hugging Face model IDs
    primary_model: str = "01-ai/Yi-1.5B-Coder"  # Yi-Coder-1.5B as primary code model
    secondary_model: str = "mistralai/Mistral-7B-Instruct-v0.2"  # Mistral-7B as secondary/fallback
    
    # Model parameters
    temperature: float = 0.2
    max_new_tokens: int = 512
    timeout_seconds: int = 30
    
    # Cache settings
    cache_enabled: bool = True
    cache_ttl_seconds: int = 3600
    
    # Evaluation settings
    evaluation_dataset_path: str = "evaluation_dataset.json"
    
    # API settings
    api_title: str = "AI Code Quality & Bug Explanation Assistant"
    api_version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()


def get_active_models() -> List[str]:
    """Get list of active models to use."""
    models = []
    if settings.primary_model:
        models.append(settings.primary_model)
    if settings.secondary_model and settings.secondary_model != settings.primary_model:
        models.append(settings.secondary_model)
    return models


def get_model_config(model_name: str) -> Dict[str, Any]:
    """Get configuration for a specific model."""
    return {
        "temperature": settings.temperature,
        "max_new_tokens": settings.max_new_tokens,
        "timeout": settings.timeout_seconds,
    }

