from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PYTHONPATH: str = "$PWD/src/"
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    SQLALCHEMY_DATABASE_URI: str = (
        "postgresql+psycopg2://user:password@localhost:5432/todo_db"
    )


settings = Settings()
