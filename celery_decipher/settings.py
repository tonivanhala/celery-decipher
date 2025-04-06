from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pg_connection_string: str = (
        "postgresql://coo:chief-of-operations@localhost:5432/operational"
    )


settings = Settings()
