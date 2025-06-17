from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = (
        "postgresql+psycopg2://user:password@localhost:5432/todo_db"
    )


settings = Settings()
