"""HTTP client for the Items API."""

import httpx


class ItemClient:
    """Client for interacting with the Items REST API."""

    def __init__(self, base_url: str = "http://127.0.0.1:8000", timeout: float = 5.0) -> None:
        # Таймаут обязателен! Иначе клиент может зависнуть навсегда.
        self.client = httpx.Client(base_url=base_url, timeout=timeout)

    def __enter__(self):
        """Support 'with' statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close connection when exiting the 'with' block."""
        self.client.close()

    def create_item(self, name: str, price: float) -> dict:
        """Create a new item and return the created object."""
        try:
            # json= автоматически ставит заголовок Content-Type: application/json
            resp = self.client.post("/items", json={"name": name, "price": price})
            resp.raise_for_status()  # Превращаем 4xx/5xx в исключение
            return resp.json()
        except httpx.HTTPStatusError as e:
            print(f"Client error (create): {e.response.status_code}")
            raise
        except httpx.RequestError as e:
            print(f"Network error (create): {e}")
            raise

    def get_item(self, item_id: int) -> dict:
        """Get an item by ID."""
        try:
            resp = self.client.get(f"/items/{item_id}")
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            print(f"Client error (get): {e.response.status_code}")
            raise
        except httpx.RequestError as e:
            print(f"Network error (get): {e}")
            raise

    def list_items(self, limit: int = 10, offset: int = 0) -> list[dict]:
        """Get a list of items with pagination."""
        try:
            resp = self.client.get("/items", params={"limit": limit, "offset": offset})
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            print(f"Client error (list): {e.response.status_code}")
            raise
        except httpx.RequestError as e:
            print(f"Network error (list): {e}")
            raise

    def search_items(self, q: str) -> list[dict]:
        """Search items by name."""
        try:
            resp = self.client.get("/items/search", params={"q": q})
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            print(f"Client error (search): {e.response.status_code}")
            raise
        except httpx.RequestError as e:
            print(f"Network error (search): {e}")
            raise

    def update_item(self, item_id: int, name: str, price: float) -> dict:
        """Update an existing item."""
        try:
            resp = self.client.put(f"/items/{item_id}", json={"name": name, "price": price})
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            print(f"Client error (update): {e.response.status_code}")
            raise
        except httpx.RequestError as e:
            print(f"Network error (update): {e}")
            raise

    def delete_item(self, item_id: int) -> None:
        """Delete an item."""
        try:
            resp = self.client.delete(f"/items/{item_id}")
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"Client error (delete): {e.response.status_code}")
            raise
        except httpx.RequestError as e:
            print(f"Network error (delete): {e}")
            raise