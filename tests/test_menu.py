import pytest
from httpx import AsyncClient
from logger import logger

from models.menu import Menu
from tests.fixtures import MENU_DATA, MENU_DATA_UPDATE


@pytest.mark.anyio
async def test_create_menu(test_db: AsyncClient) -> None:
    response = await test_db.post('/menus', json=MENU_DATA)
    logger.debug(f'response create menu {response}')
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['title'] == MENU_DATA['title']
    assert response.json()['description'] == MENU_DATA['description']
    list_menus = await test_db.get('/menus')
    assert len(list_menus.json()) == 1


@pytest.mark.anyio
async def test_get_menus(test_db: AsyncClient,
                         menu: Menu) -> None:
    response = await test_db.get('/menus')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['title'] == MENU_DATA['title']
    assert response.json()[0]['description'] == MENU_DATA['description']


@pytest.mark.anyio
async def test_get_menu(test_db: AsyncClient,
                        menu: Menu) -> None:
    menu_id = menu.id
    response = await test_db.get(f'/menus/{menu_id}')
    assert response.status_code == 200
    assert response.json()['id'] == str(menu_id)
    assert response.json()['title'] == MENU_DATA['title']
    assert response.json()['description'] == MENU_DATA['description']


@pytest.mark.anyio
async def test_update_menu(test_db: AsyncClient,
                           menu: Menu) -> None:
    menu_id = menu.id
    response = await test_db.patch(f'/menus/{menu_id}',
                                   json=MENU_DATA_UPDATE)
    assert response.status_code == 200
    update_menu = await test_db.get(f'/menus/{menu_id}')
    assert update_menu.json()['description'] == MENU_DATA_UPDATE['description']
    assert update_menu.json()['title'] == MENU_DATA_UPDATE['title']


@pytest.mark.anyio
async def test_delete_menu(test_db: AsyncClient,
                           menu: Menu) -> None:
    response = await test_db.delete(f'/menus/{menu.id}')
    assert response.status_code == 200
    assert response.json()['message'] == 'The menu has been deleted'
    menus = await test_db.get('/menus')
    assert not menus.json()
