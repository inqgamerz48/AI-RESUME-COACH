"""
Configuration settings for the application.
All sensitive data must come from environment variables.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "AI Resume Coach for Freshers"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str
    
    # AI
    HUGGINGFACE_API_KEY: str
    AI_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.2"
    AI_MAX_TOKENS: int = 150
    AI_TEMPERATURE: float = 0.7
    AI_TOP_P: float = 0.9
    
    # CORS
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    
    # Tier Limits
    FREE_AI_LIMIT: int = 3
    FREE_RESUME_LIMIT: int = 1
    PRO_AI_LIMIT: int = 50
    PRO_RESUME_LIMIT: int = 10
    ULTIMATE_AI_LIMIT: int = 9999  # Effectively unlimited
    ULTIMATE_RESUME_LIMIT: int = 9999
    
    # Payment (FUTURE - NOT IMPLEMENTED)
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    RAZORPAY_KEY_ID: Optional[str] = None
    RAZORPAY_KEY_SECRET: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
