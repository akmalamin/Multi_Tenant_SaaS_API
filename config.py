"""config.py — SaaS tier limits and global configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Multi-Tenant SaaS Inventory Engine"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "1.0.0"
    DOCS_URL: str = "/docs"

    # Tiered Subscription Quotas
    PLAN_LIMITS: dict = {
        "free": {"max_items": 5, "can_export": False},
        "pro": {"max_items": 100, "can_export": True},
        "enterprise": {"max_items": 10000, "can_export": True},
    }

    class Config:
        case_sensitive = True


settings = Settings()