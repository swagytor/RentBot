from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

root = Path(__file__).parent.parent


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    BOT_TOKEN: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def BOT_TOKEN(self):
        return self.BOT_TOKEN

    class Config:
        env_file = root / ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
