from .fixtures import SUBMENU_DATA, SUBMENU_DATA_UPDATE


def test_create_submenu(test_app, menu):
    menu_id = menu.id
    list_submenus = test_app.get(f'/api/v1/menus/{menu_id}/submenus')
    assert len(list_submenus.json()) == 0
    response = test_app.post(f'/api/v1/menus/{menu_id}/submenus',
                             json=SUBMENU_DATA)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['title'] == SUBMENU_DATA['title']
    assert response.json()['description'] == SUBMENU_DATA['description']
    list_submenus = test_app.get(f'/api/v1/menus/{menu_id}/submenus')
    assert len(list_submenus.json()) == 1


def test_get_submenus(test_app, menu, submenu):
    menu_id = menu.id
    response = test_app.get(f'/api/v1/menus/{menu_id}/submenus/')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['title'] == SUBMENU_DATA['title']
    assert response.json()[0]['description'] == SUBMENU_DATA['description']


def test_get_submenu(test_app, menu, submenu):
    menu_id = menu.id
    submenu_id = submenu.id
    response = test_app.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert response.json()['id'] == str(submenu_id)
    assert response.json()['title'] == SUBMENU_DATA['title']
    assert response.json()['description'] == SUBMENU_DATA['description']


def test_update_submenu(test_app, menu, submenu):
    menu_id = menu.id
    submenu_id = submenu.id
    response = test_app.patch(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}',
        json=SUBMENU_DATA_UPDATE)
    assert response.status_code == 200
    assert submenu.description == SUBMENU_DATA_UPDATE['description']
    assert submenu.title == SUBMENU_DATA_UPDATE['title']


def test_delete_submenu(test_app, menu, submenu):
    menu_id = menu.id
    submenu_id = submenu.id
    response = test_app.delete(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert response.json() is None
    submenus = test_app.get(f'/api/v1/menus/{menu_id}/submenus')
    assert not submenus.json()
