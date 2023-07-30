import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import uuid
from models.menu import Menu
from models.submenu import SubMenu
from models.dish import Dish
from main import app
from database import BaseDBModel, get_db
from .fixtures import MENU_DATA, SUBMENU_DATA, DISH_DATA


@pytest.fixture
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


@pytest.fixture
def menu(test_db):
    test_db.add(Menu(**MENU_DATA, id=uuid.uuid4()))
    test_db.commit()
    menu = test_db.query(Menu).first()
    return menu


@pytest.fixture
def submenu(test_db, menu):
    test_db.add(SubMenu(**SUBMENU_DATA,
                        id=uuid.uuid4(),
                        menu_id=menu.id))
    test_db.commit()
    submenu = test_db.query(SubMenu).first()
    return submenu


@pytest.fixture
def dish(test_db, submenu):
    test_db.add(Dish(**DISH_DATA,
                     id=uuid.uuid4(),
                     submenu_id=submenu.id))
    test_db.commit()
    dish = test_db.query(Dish).first()
    return dish
