import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from main import app
from database import BaseDBModel, get_db


@pytest.fixture(scope="session")
def test_db():
    engine = create_engine("postgresql://postgres:postgres@localhost:5432/menu")
    TestingSessionLocal = sessionmaker(autocommit=False,
                                       autoflush=False,
                                       bind=engine)

    BaseDBModel.metadata.create_all(bind=engine)

    yield TestingSessionLocal()

    BaseDBModel.metadata.drop_all(bind=engine)


@pytest.fixture
def test_app(test_db):

    def override_get_db():
        db = test_db
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
