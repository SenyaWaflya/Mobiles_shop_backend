from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    JWT_PRIVATE: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    JWT_PUBLIC: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
