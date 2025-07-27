"""
Configuration settings for the External Data Service.
"""
import os
import json
from typing import List, Dict, Any, Optional
from pydantic import validator, BaseModel


class Settings(BaseModel):
    """Settings for the External Data Service."""
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "External Data Service"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Cache settings
    CACHE_TTL: int = 300  # seconds
    
    # Circuit breaker settings
    CIRCUIT_BREAKER_FAILURE_THRESHOLD: int = 5
    CIRCUIT_BREAKER_RECOVERY_TIMEOUT: int = 30  # seconds
    
    # External API settings (con valores por defecto)
    NEWS_API_URL: str = "https://newsapi.org/v2"
    NEWS_API_KEY: str = "demo_api_key"
    
    TWITTER_API_URL: str = "https://api.twitter.com/2"
    TWITTER_API_KEY: str = "demo_twitter_key"
    TWITTER_API_SECRET: str = "demo_twitter_secret"
    TWITTER_BEARER_TOKEN: str = "demo_bearer_token"
    
    ECONOMIC_CALENDAR_API_URL: str = "https://example.com/economic-calendar-api"
    ECONOMIC_CALENDAR_API_KEY: str = "demo_economic_key"
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    
    # Authentication settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


# Create settings instance with environment variables
def load_settings():
    """Load settings from environment variables."""
    return Settings(
        BACKEND_CORS_ORIGINS=os.getenv("BACKEND_CORS_ORIGINS", "*"),
        NEWS_API_KEY=os.getenv("NEWS_API_KEY", "demo_api_key"),
        TWITTER_API_KEY=os.getenv("TWITTER_API_KEY", "demo_twitter_key"),
        TWITTER_API_SECRET=os.getenv("TWITTER_API_SECRET", "demo_twitter_secret"),
        TWITTER_BEARER_TOKEN=os.getenv("TWITTER_BEARER_TOKEN", "demo_bearer_token"),
        ECONOMIC_CALENDAR_API_KEY=os.getenv("ECONOMIC_CALENDAR_API_KEY", "demo_economic_key"),
        SECRET_KEY=os.getenv("SECRET_KEY", "your-secret-key-change-in-production"),
    )

settings = load_settings()
