"""Repository layer for data storage (JSON file)."""

import json
from pathlib import Path

from api_service.models import ItemCreate, ItemRead


class ItemRepository:
    """Handles saving and loading items to/from a JSON file."""

    def __init__(self, file_path: str = "data.json") -> None:
        self.file_path = Path(file_path)
        self._items: dict[int, ItemRead] = {}
        self._next_id = 1
        self._load()

    def _load(self) -> None:
        """Load data from file if it exists."""
        if self.file_path.exists():
            try:
                data = json.loads(self.file_path.read_text(encoding="utf-8"))
                for item_dict in data:
                    item = ItemRead(**item_dict)
                    self._items[item.id] = item
                if self._items:
                    self._next_id = max(self._items.keys()) + 1
            except Exception as e:
                print(f"Error loading data: {e}")

    def _save(self) -> None:
        """Save current data to file."""
        data = [item.model_dump() for item in self._items.values()]
        self.file_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False), 
            encoding="utf-8"
        )

    def create(self, item_in: ItemCreate) -> ItemRead:
        """Create a new item and save it."""
        item = ItemRead(id=self._next_id, **item_in.model_dump())
        self._items[item.id] = item
        self._next_id += 1
        self._save()
        return item

    def get_by_id(self, item_id: int) -> ItemRead | None:
        """Get a single item by ID."""
        return self._items.get(item_id)

    def get_all(self, limit: int = 10, offset: int = 0, q: str | None = None) -> list[ItemRead]:
        """Get a list of items with optional search and pagination."""
        items = list(self._items.values())
        
        if q:
            q_lower = q.lower()
            items = [i for i in items if q_lower in i.name.lower()]
            
        return items[offset : offset + limit]

    def update(self, item_id: int, item_in: ItemCreate) -> ItemRead | None:
        """Update an existing item."""
        if item_id not in self._items:
            return None
        item = ItemRead(id=item_id, **item_in.model_dump())
        self._items[item_id] = item
        self._save()
        return item

    def delete(self, item_id: int) -> bool:
        """Delete an item. Returns True if deleted, False if not found."""
        if item_id in self._items:
            del self._items[item_id]
            self._save()
            return True
        return False