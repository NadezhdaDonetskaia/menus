from tests.fixtures import DISH_DATA, DISH_DATA_UPDATE


def test_create_dish(test_app, menu, submenu):
    menu_id = menu.id
    submenu_id = submenu.id
    list_dishes = test_app.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert len(list_dishes.json()) == 0
    response = test_app.post(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
        json=DISH_DATA)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['title'] == DISH_DATA['title']
    assert response.json()['description'] == DISH_DATA['description']
    list_dishes = test_app.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert len(list_dishes.json()) == 1


def test_get_dishes(test_app, menu, submenu, dish):
    menu_id = menu.id
    submenu_id = submenu.id
    response = test_app.get(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['title'] == DISH_DATA['title']
    assert response.json()[0]['description'] == DISH_DATA['description']


def test_get_dish(test_app, menu, submenu, dish):
    menu_id = menu.id
    submenu_id = submenu.id
    dish_id = dish.id
    response = test_app.get(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    assert response.json()['id'] == str(dish_id)
    assert response.json()['title'] == DISH_DATA['title']
    assert response.json()['description'] == DISH_DATA['description']


def test_update_dish(test_app, menu, submenu, dish):
    menu_id = menu.id
    submenu_id = submenu.id
    dish_id = dish.id
    response = test_app.patch(
        f'api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
        json=DISH_DATA_UPDATE)
    assert response.status_code == 200
    assert dish.description == DISH_DATA_UPDATE['description']
    assert dish.title == DISH_DATA_UPDATE['title']


def test_delete_dish(test_app, menu, submenu, dish):
    menu_id = menu.id
    submenu_id = submenu.id
    dish_id = dish.id
    response = test_app.delete(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    assert response.json() is None
    dish = test_app.get(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert not dish.json()
