from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Tailor Management System"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: Optional[str] = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database settings
    DATABASE_URL: Optional[str] = None

    # Email settings
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[str] = None
    MAIL_PORT: Optional[int] = None
    MAIL_SERVER: Optional[str] = None
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True
    USE_CREDENTIALS: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Validate required settings
if not settings.SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in environment or .env file")

if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL must be set in environment or .env file")

# Validate email settings if any email-related functionality is used
if any([settings.MAIL_USERNAME, settings.MAIL_PASSWORD, settings.MAIL_FROM, settings.MAIL_PORT, settings.MAIL_SERVER]):
    if not all([settings.MAIL_USERNAME, settings.MAIL_PASSWORD, settings.MAIL_FROM, settings.MAIL_PORT, settings.MAIL_SERVER]):
        raise ValueError("All email settings (MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM, MAIL_PORT, MAIL_SERVER) must be set if any are provided")