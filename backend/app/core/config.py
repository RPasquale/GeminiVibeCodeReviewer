"""
Configuration settings for the Vibe Code Reviewer application.
"""

from pydantic_settings import BaseSettings
from typing import Optional, List
import os

class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "Vibe Code Reviewer"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/vibe_app"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # LLM Configuration
    llm_provider: str = "ollama"  # Options: "ollama", "openai", "anthropic", "google"
    llm_model: str = "deepseek-coder:1.3b"  # Model name for the selected provider
    
    # API Keys (for production providers)
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    
    # Ollama Configuration (for local development)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "deepseek-coder:1.3b"
    
    # MLflow
    mlflow_tracking_uri: str = "http://localhost:5000"
    
    # DSPy Configuration
    dspy_max_tokens: int = 4000
    dspy_temperature: float = 0.1
    
    # Training Configuration
    training_batch_size: int = 32
    training_epochs: int = 10
    training_learning_rate: float = 1e-5
    
    # Optimization Configuration
    optimization_max_iterations: int = 100
    optimization_metric: str = "accuracy"
    
    # File Upload
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = [
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", 
        ".h", ".hpp", ".cs", ".php", ".rb", ".go", ".rs", ".swift",
        ".kt", ".scala", ".r", ".m", ".sh", ".bash", ".zsh", ".fish"
    ]
    
    # Security
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()

# Validate required settings
def validate_settings():
    """Validate that all required settings are present."""
    if settings.llm_provider == "ollama":
        # For Ollama, we don't need API keys
        print("Using Ollama for local development")
        print(f"Ollama model: {settings.ollama_model}")
        print(f"Ollama URL: {settings.ollama_base_url}")
    else:
        # For production providers, validate API keys
        required_keys = []
        if settings.llm_provider == "openai":
            required_keys.append("openai_api_key")
        elif settings.llm_provider == "anthropic":
            required_keys.append("anthropic_api_key")
        elif settings.llm_provider == "google":
            required_keys.append("google_api_key")
        
        missing_keys = []
        for key in required_keys:
            if not getattr(settings, key):
                missing_keys.append(key)
        
        if missing_keys:
            print(f"Warning: Missing API keys for {settings.llm_provider}: {missing_keys}")
            print("Some features may not work without these keys.")

# Validate on import
validate_settings()
