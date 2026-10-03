"""app/schemas/item_schema.py — Pydantic models for Tenant-isolated inventory items."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=2, example="Pepperoni Pizza 14-inch")
    category: str = Field(..., example="Food & Beverage")
    price: float = Field(..., gt=0.0, example=18.50)
    stock: int = Field(default=10, ge=0, example=25)


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(None, gt=0.0)
    stock: Optional[int] = Field(None, ge=0)


class ItemResponse(ItemCreate):
    id: str = Field(..., example="ITEM-A1B2C3D4")
    tenant_id: str = Field(..., example="tenant_pizza_palace")
    created_at: datetime
    updated_at: datetime


class TenantInventorySummary(BaseModel):
    tenant_id: str
    tenant_name: str
    plan: str
    item_count: int
    max_limit: int
    items: List[ItemResponse]