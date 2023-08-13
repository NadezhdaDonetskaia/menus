import pytest
from logger import logger

from tests.fixtures import SUBMENU_DATA, SUBMENU_DATA_UPDATE


@pytest.mark.anyio
async def test_create_submenu(test_db, menu):
    menu_id = menu.id
    response = await test_db.post(f'/menus/{menu_id}/submenus',
                                  json=SUBMENU_DATA)
    logger.debug(f'response create submenu {response}')
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['title'] == SUBMENU_DATA['title']
    assert response.json()['description'] == SUBMENU_DATA['description']
    list_submenus = await test_db.get(f'/menus/{menu_id}/submenus')
    assert len(list_submenus.json()) == 1


@pytest.mark.anyio
async def test_get_submenus(test_db, menu, submenu):
    menu_id = menu.id
    response = await test_db.get(f'/menus/{menu_id}/submenus')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['title'] == SUBMENU_DATA['title']
    assert response.json()[0]['description'] == SUBMENU_DATA['description']


@pytest.mark.anyio
async def test_get_submenu(test_db, menu, submenu):
    menu_id = menu.id
    submenu_id = submenu.id
    response = await test_db.get(f'/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert response.json()['id'] == str(submenu_id)
    assert response.json()['title'] == SUBMENU_DATA['title']
    assert response.json()['description'] == SUBMENU_DATA['description']


@pytest.mark.anyio
async def test_update_submenu(test_db, menu, submenu):
    menu_id = menu.id
    submenu_id = submenu.id
    response = await test_db.patch(
        f'/menus/{menu_id}/submenus/{submenu_id}',
        json=SUBMENU_DATA_UPDATE)
    assert response.status_code == 200
    update_submenu = await test_db.get(f'/menus/{menu_id}/submenus/{submenu_id}')
    assert update_submenu.json()['description'] == SUBMENU_DATA_UPDATE['description']
    assert update_submenu.json()['title'] == SUBMENU_DATA_UPDATE['title']


@pytest.mark.anyio
async def test_delete_submenu(test_db, menu, submenu):
    menu_id = menu.id
    submenu_id = submenu.id
    response = await test_db.delete(
        f'/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert response.json()['message'] == 'The submenu has been deleted'
    submenus = await test_db.get(f'/menus/{menu_id}/submenus')
    assert not submenus.json()
