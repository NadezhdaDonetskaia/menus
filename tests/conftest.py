import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from logger import logger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import db_url_test
from database import get_async_db, metadata
from main import app
from models.dish import Dish
from models.menu import Menu
from models.submenu import SubMenu
from services.cache import CacheRepository
from tests.fixtures import DISH_DATA, DISH_DATA2, MENU_DATA, MENU_DATA2, SUBMENU_DATA

engine_test = create_async_engine(db_url_test)
async_session = async_sessionmaker(engine_test,
                                   class_=AsyncSession,
                                   expire_on_commit=False)
metadata.bind = engine_test


async def override_get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

app.dependency_overrides[get_async_db] = override_get_async_db


@app.get('/crear_cache')
def clear_cache():
    CacheRepository().redis.flushall()


@pytest.fixture(autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        clear_cache()


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture
@pytest.mark.anyio
async def test_db() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app,
                           base_url='http://localhost:8000/api/v1') as ac:
        yield ac


@pytest.fixture
@pytest.mark.anyio
async def menu(test_db) -> Menu:
    new_menu = await test_db.post('/menus', json=MENU_DATA)
    return Menu(**new_menu.json())


@pytest.fixture
@pytest.mark.anyio
async def menu2(test_db) -> Menu:
    new_menu = await test_db.post('/menus', json=MENU_DATA2)
    return Menu(**new_menu.json())


@pytest.fixture
@pytest.mark.anyio
async def submenu(test_db, menu) -> SubMenu:
    new_submenu = await test_db.post(
        f'/menus/{menu.id}/submenus',
        json=SUBMENU_DATA)
    logger.debug(f'response conftest create submenu {new_submenu.json()}')
    return SubMenu(**new_submenu.json())


@pytest.fixture
@pytest.mark.anyio
async def dish(test_db, menu, submenu) -> Dish:
    new_dish = await test_db.post(
        f'/menus/{menu.id}/submenus/{submenu.id}/dishes',
        json=DISH_DATA
    )
    logger.debug(f'response conftest create dish {new_dish.json()}')
    return Dish(**new_dish.json())


@pytest.fixture
async def dish2(test_db, menu, submenu) -> Dish:
    new_dish = await test_db.post(
        f'/menus/{menu.id}/submenus/{submenu.id}/dishes',
        json=DISH_DATA2
    )
    return Dish(**new_dish.json())
