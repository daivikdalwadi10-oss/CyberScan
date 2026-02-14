from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "CyberSec SaaS"
    environment: str = "development"  # 'production' or 'development'
    secret_key: str = Field(..., min_length=32)
    algorithm: str = "HS256"
    access_token_expires_minutes: int = 30
    refresh_token_expires_days: int = 7
    database_url: str = Field(..., min_length=10)
    cors_origins: str = "http://localhost:5173"
    allowed_hosts: str = "localhost,127.0.0.1,::1"
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60
    log_level: str = "INFO"
    security_headers_enabled: bool = True
    hsts_enabled: bool = False

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[1] / ".env"),
        env_file_encoding="utf-8",
    )

    def validate_for_production(self):
        if self.environment == "production":
            if not self.secret_key or len(self.secret_key) < 32 or "secret" in self.secret_key:
                raise ValueError("SECRET_KEY must be set to a strong, random value in production.")
            if "localhost" in self.cors_origins or "127.0.0.1" in self.cors_origins:
                raise ValueError("CORS_ORIGINS must not allow localhost in production.")
            if "localhost" in self.allowed_hosts or "127.0.0.1" in self.allowed_hosts:
                raise ValueError("ALLOWED_HOSTS must not allow localhost in production.")
            if not self.hsts_enabled:
                raise ValueError("HSTS must be enabled in production for HTTPS enforcement.")

settings = Settings()
