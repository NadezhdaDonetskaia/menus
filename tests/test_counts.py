def test_counts(test_app, menu, submenu, dish, dish2):
    menu_id = menu.id
    submenu_id = submenu.id

    menu = test_app.get(f'/api/v1/menus/{menu_id}')
    assert menu.json()['submenus_count'] == 1
    assert menu.json()['dishes_count'] == 2

    submenu = test_app.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert submenu.json()['dishes_count'] == 2

    test_app.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')

    submenus = test_app.get(f'/api/v1/menus/{menu_id}/submenus')
    assert submenus.status_code == 200
    assert not submenus.json()

    dishes = test_app.get(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert dishes.status_code == 200
    assert not dishes.json()

    menu = test_app.get(f'/api/v1/menus/{menu_id}')
    assert menu.json()['submenus_count'] == 0
    assert menu.json()['dishes_count'] == 0
