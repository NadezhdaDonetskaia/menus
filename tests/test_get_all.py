import pytest
from httpx import AsyncClient

from models.dish import Dish
from models.menu import Menu
from models.submenu import SubMenu
from tests.fixtures import ALL_DATA, ALL_DATA_WITHOUT_DISH


@pytest.mark.anyio
async def test_counts(test_db: AsyncClient,
                      menu: Menu,
                      submenu: SubMenu,
                      dish: Dish,
                      dish2: Dish) -> None:
    menu_id = menu.id
    submenu_id = submenu.id
    dish_id = dish.id

    all = await test_db.get(url='')
    assert all.json() == ALL_DATA

    await test_db.delete(f'/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')

    all_without_dish = await test_db.get(url='')
    assert all_without_dish.json() == ALL_DATA_WITHOUT_DISH

    await test_db.delete(f'/menus/{menu_id}')
    all = await test_db.get(url='')
    assert all.json() == {}
