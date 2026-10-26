"""Tests for the FastAPI application."""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path

from api_service.app import app, repo

# TestClient — это "виртуальный клиент", который общается с app напрямую
client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_repository(tmp_path: Path) -> None:
    """
    Fixture runs before each test.
    It replaces the real data.json with a temporary empty file
    and clears the in-memory dictionary.
    """
    repo.file_path = tmp_path / "test_data.json"
    repo._items = {}
    repo._next_id = 1


def test_create_item() -> None:
    """Test creating a new item returns 201 and the item with ID."""
    response = client.post("/items", json={"name": "Apple", "price": 10.5})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Apple"
    assert data["price"] == 10.5
    assert "id" in data


def test_get_item() -> None:
    """Test getting an existing item returns 200."""
    # Create item first
    create_resp = client.post("/items", json={"name": "Banana", "price": 5.0})
    item_id = create_resp.json()["id"]

    # Get it
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Banana"


def test_get_non_existent_item() -> None:
    """Test getting a non-existent item returns 404."""
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "item not found"


def test_create_item_invalid_name() -> None:
    """Test that empty name returns 422 (Pydantic validation)."""
    response = client.post("/items", json={"name": "", "price": 10.5})
    assert response.status_code == 422


def test_create_item_invalid_price() -> None:
    """Test that negative price returns 422 (Pydantic validation)."""
    response = client.post("/items", json={"name": "Apple", "price": -5})
    assert response.status_code == 422


def test_list_items_and_search() -> None:
    """Test list with pagination and search."""
    # Create 3 items
    client.post("/items", json={"name": "Apple", "price": 10})
    client.post("/items", json={"name": "Banana", "price": 20})
    client.post("/items", json={"name": "Apricot", "price": 30})

    # Test list (limit 2)
    resp_list = client.get("/items?limit=2&offset=0")
    assert resp_list.status_code == 200
    assert len(resp_list.json()) == 2

    # Test search (q="Ap")
    resp_search = client.get("/items/search?q=Ap")
    assert resp_search.status_code == 200
    results = resp_search.json()
    assert len(results) == 2
    assert results[0]["name"] == "Apple"
    assert results[1]["name"] == "Apricot"


def test_update_item() -> None:
    """Test updating an item returns 200."""
    create_resp = client.post("/items", json={"name": "Old", "price": 1})
    item_id = create_resp.json()["id"]

    response = client.put(f"/items/{item_id}", json={"name": "New", "price": 2})
    assert response.status_code == 200
    assert response.json()["name"] == "New"
    assert response.json()["price"] == 2


def test_delete_item() -> None:
    """Test deleting an item returns 204 and it's gone."""
    create_resp = client.post("/items", json={"name": "To Delete", "price": 1})
    item_id = create_resp.json()["id"]

    # Delete
    resp_delete = client.delete(f"/items/{item_id}")
    assert resp_delete.status_code == 204

    # Check it's gone
    resp_get = client.get(f"/items/{item_id}")
    assert resp_get.status_code == 404