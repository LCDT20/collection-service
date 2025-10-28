from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = Field(
        ...,
        description="MySQL database connection URL"
    )
    
    # JWT Authentication
    AUTH_JWKS_URL: str = Field(
        ...,
        description="JWKS URL for JWT verification"
    )
    
    JWT_AUDIENCE: str = Field(
        default="collection-service",
        description="Expected JWT audience"
    )
    
    JWT_ISSUER: str = Field(
        default="https://auth.takeyourtrade.com",
        description="Expected JWT issuer"
    )
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=[
            "https://app.takeyourtrade.com",
            "https://takeyourtrade.com",
            "https://www.takeyourtrade.com",
            "http://localhost:3000",
            "http://localhost:8000"
        ],
        description="Allowed CORS origins"
    )
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            # Handle JSON array string
            import json
            return json.loads(v)
        return v
    
    # Application
    APP_NAME: str = Field(
        default="Collection Service",
        description="Application name"
    )
    
    APP_VERSION: str = Field(
        default="1.0.0",
        description="Application version"
    )
    
    DEBUG: bool = Field(
        default=False,
        description="Debug mode"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

