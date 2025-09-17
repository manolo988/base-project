import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.core.config import settings
from app.repositories.user import user_repository
from app.schemas.user import UserCreate

# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db() -> Generator:
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client(db) -> Generator:
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_user(db):
    user = user_repository.create(
        db,
        obj_in=UserCreate(
            email="test@example.com",
            password="testpassword",
            full_name="Test User"
        )
    )
    return user


@pytest.fixture
def test_superuser(db):
    user = user_repository.create(
        db,
        obj_in=UserCreate(
            email="superuser@example.com",
            password="superpassword",
            full_name="Super User",
            is_superuser=True
        )
    )
    return user


@pytest.fixture
def test_user_token(client, test_user):
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": test_user.email,
            "password": "testpassword"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
def test_superuser_token(client, test_superuser):
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": test_superuser.email,
            "password": "superpassword"
        }
    )
    return response.json()["access_token"]