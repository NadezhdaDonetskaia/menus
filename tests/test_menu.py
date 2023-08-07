from .fixtures import MENU_DATA, MENU_DATA_UPDATE


def test_create_menu(test_app):
    list_menus = test_app.get('/api/v1/menus')
    assert len(list_menus.json()) == 0
    response = test_app.post('/api/v1/menus', json=MENU_DATA)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['title'] == MENU_DATA['title']
    assert response.json()['description'] == MENU_DATA['description']
    list_menus = test_app.get('/api/v1/menus')
    assert len(list_menus.json()) == 1


def test_get_menus(test_app, menu):
    response = test_app.get('/api/v1/menus')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['title'] == MENU_DATA['title']
    assert response.json()[0]['description'] == MENU_DATA['description']


def test_get_menu(test_app, menu):
    menu_id = menu.id
    response = test_app.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert response.json()['id'] == str(menu_id)
    assert response.json()['title'] == MENU_DATA['title']
    assert response.json()['description'] == MENU_DATA['description']


def test_update_menu(test_app, menu):
    menu_id = menu.id
    response = test_app.patch(f'/api/v1/menus/{menu_id}',
                              json=MENU_DATA_UPDATE)
    assert response.status_code == 200
    assert menu.description == MENU_DATA_UPDATE['description']
    assert menu.title == MENU_DATA_UPDATE['title']


def test_delete_menu(test_app, menu):
    response = test_app.delete(f'/api/v1/menus/{menu.id}')
    assert response.status_code == 200
    assert response.json() is None
    menus = test_app.get('/api/v1/menus')
    assert not menus.json()
