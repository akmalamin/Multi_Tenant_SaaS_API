"""app/services/item_service.py — Tenant-scoped item management and quota enforcement."""

import uuid
from datetime import datetime
from typing import List, Optional
from app.db.tenant_db import db
from app.schemas.item_schema import ItemCreate, ItemUpdate


class ItemService:

    @staticmethod
    def get_tenant_items(tenant: dict) -> List[dict]:
        """Fetch all items belonging ONLY to this tenant."""
        return db.list_items_for_tenant(tenant["id"])

    @staticmethod
    def create_item(tenant: dict, item_in: ItemCreate) -> dict:
        """Enforces plan limits before allowing item creation."""
        current_items = db.list_items_for_tenant(tenant["id"])
        max_allowed = tenant["max_items_allowed"]

        if len(current_items) >= max_allowed:
            raise ValueError(
                f"Plan quota exceeded! '{tenant['name']}' is on the '{tenant['plan'].upper()}' tier "
                f"(Max: {max_allowed} items). Upgrade plan to create more."
            )

        new_id = f"ITEM-{str(uuid.uuid4())[:8].upper()}"
        now = datetime.utcnow()

        item_record = {
            "id": new_id,
            "tenant_id": tenant["id"],
            **item_in.model_dump(),
            "created_at": now,
            "updated_at": now,
        }
        return db.create_item(item_record)

    @staticmethod
    def get_single_item(item_id: str, tenant: dict) -> Optional[dict]:
        return db.get_item_for_tenant(item_id, tenant["id"])

    @staticmethod
    def update_item(item_id: str, tenant: dict, item_in: ItemUpdate) -> Optional[dict]:
        update_data = item_in.model_dump(exclude_unset=True)
        return db.update_item_for_tenant(item_id, tenant["id"], update_data)

    @staticmethod
    def delete_item(item_id: str, tenant: dict) -> bool:
        return db.delete_item_for_tenant(item_id, tenant["id"])