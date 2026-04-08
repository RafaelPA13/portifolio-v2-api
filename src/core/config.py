from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    # Banco de dados
    DATABASE_URL: str
    
    # Supabase Storage
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_BUCKET: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    class Config:
        env_file = str(BASE_DIR / ".env")
        
settings = Settings()