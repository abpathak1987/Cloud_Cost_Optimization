# src/cloud_cost_optimizer/config/settings.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    DATABASE_URL: str = "sqlite:///./cloud_costs.db"
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Cloud Cost Optimizer"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Cloud Provider
    CLOUD_PROVIDER: str = "dummy"  # For POC
    
    # ML Model
    MODEL_PATH: Optional[str] = None
    PREDICTION_HORIZON_DAYS: int = 7
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
