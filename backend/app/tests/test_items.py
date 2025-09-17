import pytest
from fastapi.testclient import TestClient
from app.core.config import settings


def test_create_item(client: TestClient, test_user_token):
    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={
            "title": "Test Item",
            "description": "Test Description",
            "price": 99.99
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Item"
    assert data["description"] == "Test Description"
    assert data["price"] == 99.99


def test_read_items(client: TestClient, test_user_token):
    response = client.get(
        f"{settings.API_V1_STR}/items/",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "pages" in data


def test_read_item(client: TestClient, test_user_token):
    # Create an item first
    create_response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={"title": "Test Item"}
    )
    item_id = create_response.json()["id"]

    # Read the item
    response = client.get(
        f"{settings.API_V1_STR}/items/{item_id}",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["title"] == "Test Item"


def test_update_item(client: TestClient, test_user_token):
    # Create an item first
    create_response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={"title": "Test Item"}
    )
    item_id = create_response.json()["id"]

    # Update the item
    response = client.put(
        f"{settings.API_V1_STR}/items/{item_id}",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={"title": "Updated Item", "price": 199.99}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Item"
    assert data["price"] == 199.99


def test_delete_item(client: TestClient, test_user_token):
    # Create an item first
    create_response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={"title": "Test Item"}
    )
    item_id = create_response.json()["id"]

    # Delete the item
    response = client.delete(
        f"{settings.API_V1_STR}/items/{item_id}",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200

    # Verify item is deleted
    get_response = client.get(
        f"{settings.API_V1_STR}/items/{item_id}",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert get_response.status_code == 404


def test_unauthorized_access(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/items/")
    assert response.status_code == 401