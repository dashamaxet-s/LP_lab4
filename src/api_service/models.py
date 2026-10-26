"""Pydantic models for input and output."""

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    """Model for creating a new item (client input, no id)."""
    
    name: str = Field(
        min_length=1, 
        max_length=64, 
        description="Item name (1-64 chars)"
    )
    price: float = Field(
        gt=0, 
        description="Item price (must be greater than 0)"
    )


class ItemRead(ItemCreate):
    """Model for returning an item (server output, with id)."""
    
    id: int = Field(
        description="Unique identifier assigned by the server"
    )