
# from fastapi.testclient import TestClient
# from main import app


MENU_DATA = {"title": "Test Menu", "description": "Test Description"}


# client = TestClient(app)


def test_menu(test_app):
    response = test_app.post("/api/v1/menus", json=MENU_DATA)
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["title"] == MENU_DATA["title"]
    assert response.json()["description"] == MENU_DATA["description"]


    # response = client.get("/api/v1/menus")
