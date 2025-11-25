"""Configuration management for the AI Debugging Assistant backend."""
import os
from typing import List, Dict, Any
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Hugging Face API
    hf_api_key: str = os.getenv("HF_API_KEY", "")
    hf_api_base: str = "https://router.huggingface.co/v1/chat/completions"  # New router endpoint (OpenAI-compatible)
    
    # Model configuration - Qwen code-specific models only
    # Using Qwen models optimized for code analysis and debugging
    # Router API supports specific models - check https://huggingface.co/docs/api-inference for available models
    primary_model: str = "Qwen/Qwen2.5-Coder-7B-Instruct"  # Qwen code-specific model, 7B parameters
    secondary_model: str = "Qwen/Qwen2.5-Coder-1.5B-Instruct"  # Qwen code-specific model, 1.5B parameters (if available)
    
    # Model parameters
    temperature: float = 0.2
    max_new_tokens: int = 512
    timeout_seconds: int = 30
    
    # Cache settings
    cache_enabled: bool = True  # Can be overridden via CACHE_ENABLED env var
    cache_max_size: int = 512  # Can be overridden via CACHE_MAX_SIZE env var
    cache_default_ttl_seconds: int = 3600  # Can be overridden via CACHE_DEFAULT_TTL_SECONDS env var
    
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

