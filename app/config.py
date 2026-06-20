from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configurações da aplicação, lidas automaticamente do arquivo .env
    """
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "cadastro_clientes"

    class Config:
        env_file = ".env"


settings = Settings()
