import pytest
from httpx import AsyncClient
from logger import logger

from models.dish import Dish
from models.menu import Menu
from models.submenu import SubMenu
from tests.fixtures import DISH_DATA, DISH_DATA_UPDATE


@pytest.mark.anyio
async def test_create_dish(test_db: AsyncClient,
                           menu: Menu,
                           submenu: SubMenu) -> None:
    menu_id = menu.id
    submenu_id = submenu.id
    response = await test_db.post(
        f'/menus/{menu_id}/submenus/{submenu_id}/dishes',
        json=DISH_DATA)
    logger.debug(f'response create dish {response}')
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['title'] == DISH_DATA['title']
    assert response.json()['description'] == DISH_DATA['description']
    list_dishes = await test_db.get(f'/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert len(list_dishes.json()) == 1


@pytest.mark.anyio
async def test_get_dishes(test_db: AsyncClient,
                          menu: Menu,
                          submenu: SubMenu,
                          dish: Dish) -> None:
    menu_id = menu.id
    submenu_id = submenu.id
    response = await test_db.get(
        f'/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['title'] == DISH_DATA['title']
    assert response.json()[0]['description'] == DISH_DATA['description']


@pytest.mark.anyio
async def test_get_dish(test_db: AsyncClient,
                        menu: Menu,
                        submenu: SubMenu,
                        dish: Dish) -> None:
    menu_id = menu.id
    submenu_id = submenu.id
    dish_id = dish.id
    response = await test_db.get(
        f'/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    assert response.json()['id'] == str(dish_id)
    assert response.json()['title'] == DISH_DATA['title']
    assert response.json()['description'] == DISH_DATA['description']


@pytest.mark.anyio
async def test_update_dish(test_db: AsyncClient,
                           menu: Menu,
                           submenu: SubMenu,
                           dish: Dish) -> None:
    menu_id = menu.id
    submenu_id = submenu.id
    dish_id = dish.id
    response = await test_db.patch(
        f'/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
        json=DISH_DATA_UPDATE)
    assert response.status_code == 200
    update_dish = await test_db.get(
        f'/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )
    assert update_dish.json()['description'] == DISH_DATA_UPDATE['description']
    assert update_dish.json()['title'] == DISH_DATA_UPDATE['title']


@pytest.mark.anyio
async def test_delete_dish(test_db: AsyncClient,
                           menu: Menu,
                           submenu: SubMenu,
                           dish: Dish) -> None:
    menu_id = menu.id
    submenu_id = submenu.id
    dish_id = dish.id
    response = await test_db.delete(
        f'/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    assert response.json()['message'] == 'The dish has been deleted'
    dish = await test_db.get(
        f'/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert not dish.json()
