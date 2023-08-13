import pytest


@pytest.mark.anyio
async def test_counts(test_db, menu, submenu, dish, dish2):
    menu_id = menu.id
    submenu_id = submenu.id

    menu = await test_db.get(f'/menus/{menu_id}')
    assert menu.json()['submenus_count'] == 1
    assert menu.json()['dishes_count'] == 2

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
