from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/aptitude_db"
    SECRET_KEY: str = "change-me-in-production-use-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"
    CORS_ORIGINS: str = "http://localhost:5174,http://localhost:3000"
    TEST_DURATION_MINUTES: int = 30
    TEST_TOTAL_QUESTIONS: int = 30
    TEST_EASY_COUNT: int = 15
    TEST_MEDIUM_COUNT: int = 15
    PASS_PERCENTAGE: float = 50.0

    class Config:
        env_file = ".env"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
