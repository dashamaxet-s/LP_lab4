"""FastAPI application with CRUD routes."""

from fastapi import FastAPI, HTTPException, status

from api_service.models import ItemCreate, ItemRead
from api_service.repository import ItemRepository

app = FastAPI(title="Items API", description="Lab 4 REST Service")

# Создаём один репозиторий на всё приложение
repo = ItemRepository()


@app.post(
    "/items", 
    response_model=ItemRead, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item"
)
def create_item(item: ItemCreate) -> ItemRead:
    """Create a new item and return it with the assigned ID."""
    return repo.create(item)


@app.get(
    "/items", 
    response_model=list[ItemRead],
    summary="List items with pagination"
)
def list_items(limit: int = 10, offset: int = 0) -> list[ItemRead]:
    """Get a list of items with limit and offset."""
    return repo.get_all(limit=limit, offset=offset)


# ВАЖНО: Маршрут /items/search должен быть ВЫШЕ, чем /items/{item_id}
# Иначе FastAPI подумает, что "search" — это ID товара
@app.get(
    "/items/search", 
    response_model=list[ItemRead],
    summary="Search items by name"
)
def search_items(q: str) -> list[ItemRead]:
    """Search items by substring in the name."""
    return repo.get_all(q=q)


@app.get(
    "/items/{item_id}", 
    response_model=ItemRead,
    summary="Get a single item by ID"
)
def get_item(item_id: int) -> ItemRead:
    """Get a single item by ID. Returns 404 if not found."""
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="item not found"
        )
    return item


@app.put(
    "/items/{item_id}", 
    response_model=ItemRead,
    summary="Update an existing item"
)
def update_item(item_id: int, item_in: ItemCreate) -> ItemRead:
    """Update an item. Returns 404 if not found."""
    item = repo.update(item_id, item_in)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="item not found"
        )
    return item


@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item"
)
def delete_item(item_id: int) -> None:
    """Delete an item. Returns 404 if not found."""
    success = repo.delete(item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="item not found"
        )