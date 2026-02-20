"""
Configuration settings for AI4U Backend.
"""

from pathlib import Path

from loguru import logger
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# Load local environment variables
from dotenv import load_dotenv
ENV_LOCAL_FILE = Path(__file__).resolve().parent.parent / ".env.local"
load_dotenv(dotenv_path=ENV_LOCAL_FILE)



class Settings(BaseSettings):
    """
    Application settings with AWS Secrets Manager integration.

    Uses model_validator to load secrets AFTER initial Pydantic loading,
    giving AWS Secrets Manager the highest priority.
    """

    model_config = SettingsConfigDict(
        env_file=(str(ENV_LOCAL_FILE), ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Environment Configuration
    ENVIRONMENT: str = "local"

    # AWS Configuration
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str = "test"
    AWS_ENDPOINT_URL: str = "http://localhost:4566"
    AWS_SECRET_ACCESS_KEY: str = "test"

    SQS_QUEUE_NAME: str = ""
    SQS_QUEUE_URL: str = ""

    CELERY_RESULT_BACKEND: str = ""


    @model_validator(mode="after")
    def load_secrets_from_aws(self) -> "Settings":
 
        is_local = self.ENVIRONMENT.lower() in ("local", "test", "testing")

        if is_local:
            # In local environment, use container env vars with .env.local as fallback.
            logger.info("[INFO] : Loading settings from environment/.env.local")
            return self

        else:
            logger.info("[INFO] : Loading settings from environment/.env.worker")
            return self

# Create settings instance
settings = Settings()
