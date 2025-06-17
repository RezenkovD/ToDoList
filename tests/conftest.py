import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from src.core.config import settings
from src.database.base_model import Base
from src.database.database import get_db
from src.main import app as main_app

TEST_DATABASE_URI = settings.SQLALCHEMY_DATABASE_URI

engine = create_engine(TEST_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


main_app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def connection():
    with engine.connect() as connection:
        SessionLocal.configure(bind=connection)
        yield connection


@pytest.fixture(scope="function", autouse=True)
def _transaction_wrap(connection):
    transaction = connection.begin()
    try:
        yield connection
    finally:
        transaction.rollback()


@pytest.fixture(scope="function")
def session():
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    if "test" not in TEST_DATABASE_URI:
        raise ValueError("Please connect the test database!")
    try:
        if database_exists(TEST_DATABASE_URI):
            drop_database(TEST_DATABASE_URI)
        create_database(TEST_DATABASE_URI)
        yield
    finally:
        drop_database(TEST_DATABASE_URI)


client = TestClient(main_app)
