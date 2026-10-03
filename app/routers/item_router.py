"""app/routers/item_router.py — Tenant-Isolated Inventory Endpoints."""

from fastapi import APIRouter, HTTPException, status, Depends, Path
from typing import List

from app.schemas.item_schema import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
    TenantInventorySummary
)
from app.services.item_service import ItemService
from app.middleware.tenant_context import get_current_tenant

router = APIRouter(prefix="/items", tags=["Tenant Inventory (Isolated)"])


@router.get("", response_model=TenantInventorySummary)
def get_tenant_items(current_tenant: dict = Depends(get_current_tenant)):
    """
    List all items for the tenant specified in `X-Tenant-ID` header.
    Guarantees 100% data isolation from other businesses!
    """
    items = ItemService.get_tenant_items(current_tenant)
    return {
        "tenant_id": current_tenant["id"],
        "tenant_name": current_tenant["name"],
        "plan": current_tenant["plan"],
        "item_count": len(items),
        "max_limit": current_tenant["max_items_allowed"],
        "items": items
    }


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item_in: ItemCreate,
    current_tenant: dict = Depends(get_current_tenant)
):
    """
    Create a new item in the tenant's private inventory.
    Auto-enforces subscription tier quotas (e.g. Free Tier limit = 5 items).
    """
    try:
        return ItemService.create_item(current_tenant, item_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))


@router.get("/{item_id}", response_model=ItemResponse)
def get_single_item(
    item_id: str = Path(...),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Retrieve an item by ID (ONLY if it belongs to the authenticated tenant)."""
    item = ItemService.get_single_item(item_id, current_tenant)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item '{item_id}' not found in tenant workspace '{current_tenant['id']}'."
        )
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: str = Path(...),
    current_tenant: dict = Depends(get_current_tenant)
):
    """Delete an item from the tenant's workspace."""
    deleted = ItemService.delete_item(item_id, current_tenant)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item '{item_id}' not found in tenant workspace '{current_tenant['id']}'."
        )
    return None