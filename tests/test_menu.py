from .fixtures import MENU_DATA, MENU_DATA_UPDATE


def test_create_menu(test_app):
    response = test_app.post("/api/v1/menus", json=MENU_DATA)
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["title"] == MENU_DATA["title"]
    assert response.json()["description"] == MENU_DATA["description"]


def test_get_menus(test_app, menu):
    response = test_app.get("/api/v1/menus")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == MENU_DATA["title"]
    assert response.json()[0]["description"] == MENU_DATA["description"]


def test_get_menu(test_app, menu):
    menu_id = menu.id
    response = test_app.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json()["title"] == MENU_DATA["title"]
    assert response.json()["description"] == MENU_DATA["description"]


def test_update_menu(test_app, menu, test_db):
    menu_id = menu.id
    response = test_app.patch(f"/api/v1/menus/{menu_id}",
                              json=MENU_DATA_UPDATE)
    assert response.status_code == 200
    assert menu.description == MENU_DATA_UPDATE["description"]
    assert menu.title == MENU_DATA_UPDATE["title"]


def test_delete_menu(test_app, menu):
    assert menu.title == "Test Menu"
    assert menu.description == "Test Description"
    response = test_app.delete(f"/api/v1/menus/{menu.id}")
    assert response.status_code == 200
    assert response.json() is None
