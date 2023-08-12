import pytest
from httpx import AsyncClient

from tests.fixtures import MENU_DATA, MENU_DATA_UPDATE


@pytest.mark.anyio
async def test_create_menu(test_db):
    list_menus = await test_db.get('/api/v1/menus')
    assert len(list_menus.json()) == 0
    response = await test_db.post('/api/v1/menus', json=MENU_DATA)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['title'] == MENU_DATA['title']
    assert response.json()['description'] == MENU_DATA['description']
    list_menus = await test_db.get('/api/v1/menus')
    assert len(list_menus.json()) == 1


@pytest.mark.anyio
async def test_get_menus(test_db, menu):
    response = await test_db.get('/api/v1/menus')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['title'] == MENU_DATA['title']
    assert response.json()[0]['description'] == MENU_DATA['description']


@pytest.mark.anyio
async def test_get_menu(test_db, menu):
    menu_id = menu.id
    response = await test_db.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert response.json()['id'] == str(menu_id)
    assert response.json()['title'] == MENU_DATA['title']
    assert response.json()['description'] == MENU_DATA['description']


@pytest.mark.anyio
async def test_update_menu(test_db, menu):
    menu_id = menu.id
    response = await test_db.patch(f'/api/v1/menus/{menu_id}',
                                   json=MENU_DATA_UPDATE)
    assert response.status_code == 200
    assert menu.description == MENU_DATA_UPDATE['description']
    assert menu.title == MENU_DATA_UPDATE['title']


@pytest.mark.anyio
async def test_delete_menu(test_db, menu):
    response = await test_db.delete(f'/api/v1/menus/{menu.id}')
    assert response.status_code == 200
    assert response.json() is None
    menus = await test_db.get('/api/v1/menus')
    assert not menus.json()
