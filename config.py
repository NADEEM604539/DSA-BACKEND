"""
config.py
TiDB Cloud configuration with SSL support
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ----- TiDB Cloud DB -----
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: int = Field(4000, env="DB_PORT")
    DB_NAME: str = Field(..., env="DB_NAME")

    # SSL Certificate (isrgrootx1.pem)
    DB_SSL_CA: str = Field("isrgrootx1.pem", env="DB_SSL_CA")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            f"?charset=utf8mb4"
        )


settings = Settings()