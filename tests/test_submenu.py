from .fixtures import SUBMENU_DATA, SUBMENU_DATA_UPDATE


def test_create_submenu(test_app, menu):
    menu_id = menu.id
    response = test_app.post(f"/api/v1/menus/{menu_id}/submenus",
                             json=SUBMENU_DATA)
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["title"] == SUBMENU_DATA["title"]
    assert response.json()["description"] == SUBMENU_DATA["description"]


def test_get_submenus(test_app, menu, submenu):
    menu_id = menu.id
    response = test_app.get(f"/api/v1/menus/{menu_id}/submenus/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == SUBMENU_DATA["title"]
    assert response.json()[0]["description"] == SUBMENU_DATA["description"]


def test_get_submenu(test_app, menu, submenu):
    menu_id = menu.id
    submenu_id = submenu.id
    response = test_app.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert response.json()["title"] == SUBMENU_DATA["title"]
    assert response.json()["description"] == SUBMENU_DATA["description"]


def test_update_submenu(test_app, menu, test_db):
    menu_id = menu.id
    response = test_app.patch(f"/api/v1/menus/{menu_id}",
                              json=SUBMENU_DATA_UPDATE)
    assert response.status_code == 200
    assert menu.description == SUBMENU_DATA_UPDATE["description"]
    assert menu.title == SUBMENU_DATA_UPDATE["title"]


def test_delete_menu(test_app, menu):
    assert menu.title == "Test Menu"
    assert menu.description == "Test Description"
    response = test_app.delete(f"/api/v1/menus/{menu.id}")
    assert response.status_code == 200
    assert response.json() is None