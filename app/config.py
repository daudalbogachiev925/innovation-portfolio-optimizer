from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@db:5432/innovation"
    DISCOUNT_RATE: float = 0.10
    DEFAULT_BUDGET: float = 100.0
    MAX_HIGH_RISK_SHARE: float = 0.3

    class Config:
        env_file = ".env"

settings = Settings()
