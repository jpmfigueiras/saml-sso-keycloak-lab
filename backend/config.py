from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    # Application
    app_name: str = "app1"
    app_version: str = "1.0.0"
    debug: bool = True
    environment: str = "development"
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    # Security
    secret_key: str = "dev-secret-key-change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:8080"
    # Database
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "gid"
    # Logging
    log_level: str = "INFO"
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    @property
    def database_url(self) -> str:
        """Build MySQL database URL from components"""
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    class Config:
        '''
        Configuration for Pydantic settings.
        '''
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
settings = Settings()
