import asyncio
import uuid
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import db_url_test
from database import get_async_db, metadata
from main import app
from models.dish import Dish
from models.menu import Menu
from models.submenu import SubMenu
from tests.fixtures import DISH_DATA, DISH_DATA2, MENU_DATA, SUBMENU_DATA

engine_test = create_async_engine(db_url_test)
async_session = async_sessionmaker(engine_test,
                                   class_=AsyncSession,
                                   expire_on_commit=False)
metadata.bind = engine_test


async def override_get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

app.dependency_overrides[get_async_db] = override_get_async_db


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope='session')
async def test_db() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app) as ac:
        yield ac


@pytest.fixture
async def menu(test_db):
    new_menu = await test_db.post('/api/v1/menus', MENU_DATA)
    return new_menu


# @pytest.fixture
# async def submenu(test_db, menu):
#     test_db.add(SubMenu(**SUBMENU_DATA,
#                         id=uuid.uuid4(),
#                         menu_id=menu.id))
#     test_db.commit()
#     submenu = test_db.query(SubMenu).first()
#     return submenu


# @pytest.fixture
# async def dish(test_db, submenu):
#     test_db.add(Dish(**DISH_DATA,
#                      id=uuid.uuid4(),
#                      submenu_id=submenu.id))
#     test_db.commit()
#     dish = test_db.query(Dish).first()
#     return dish


# @pytest.fixture
# async def dish2(test_db, submenu):
#     test_db.add(Dish(**DISH_DATA2,
#                      id=uuid.uuid4(),
#                      submenu_id=submenu.id))
#     test_db.commit()
#     dish = test_db.query(Dish).first()
#     return dish
