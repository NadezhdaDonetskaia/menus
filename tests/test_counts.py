import pytest
from httpx import AsyncClient

from models.dish import Dish
from models.menu import Menu
from models.submenu import SubMenu


@pytest.mark.anyio
async def test_counts(test_db: AsyncClient,
                      menu: Menu,
                      menu2: Menu,
                      submenu: SubMenu,
                      dish: Dish,
                      dish2: Dish) -> None:
    menu_id = menu.id
    submenu_id = submenu.id
    menu2_id = menu2.id

    menu = await test_db.get(f'/menus/{menu_id}')
    assert menu.json()['submenus_count'] == 1
    assert menu.json()['dishes_count'] == 2

    menu2 = await test_db.get(f'/menus/{menu2_id}')
    assert menu2.json()['submenus_count'] == 0
    assert menu2.json()['dishes_count'] == 0

    submenu = await test_db.get(f'/menus/{menu_id}/submenus/{submenu_id}')
    assert submenu.json()['dishes_count'] == 2

    await test_db.delete(f'/menus/{menu_id}/submenus/{submenu_id}')

    submenus = await test_db.get(f'/menus/{menu_id}/submenus')
    assert submenus.status_code == 200
    assert not submenus.json()

    dishes = await test_db.get(
        f'/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert dishes.status_code == 200
    assert not dishes.json()

    menu = await test_db.get(f'/menus/{menu_id}')
    assert menu.json()['submenus_count'] == 0
    assert menu.json()['dishes_count'] == 0
