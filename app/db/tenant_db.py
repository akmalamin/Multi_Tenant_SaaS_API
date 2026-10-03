"""
app/db/tenant_db.py — In-Memory Multi-Tenant Relational Datastore.

Maintains strict isolation between tenants.
Every item record is irrevocably bound to a tenant_id.
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from config import settings


class MultiTenantDB:
    def __init__(self):
        self._tenants: Dict[str, Dict[str, Any]] = {}
        self._items: Dict[str, Dict[str, Any]] = {}
        self._seed_tenants()

    def _seed_tenants(self):
        """Seed 2 distinct businesses with different subscription plans."""
        now = datetime.utcnow()
        self._tenants["tenant_pizza_palace"] = {
            "id": "tenant_pizza_palace",
            "name": "Pizza Palace",
            "admin_email": "mario@pizzapalace.com",
            "plan": "free",
            "max_items_allowed": settings.PLAN_LIMITS["free"]["max_items"],
            "is_active": True,
            "created_at": now,
        }
        self._tenants["tenant_sneaker_hub"] = {
            "id": "tenant_sneaker_hub",
            "name": "Sneaker Hub Global",
            "admin_email": "kicks@sneakerhub.io",
            "plan": "pro",
            "max_items_allowed": settings.PLAN_LIMITS["pro"]["max_items"],
            "is_active": True,
            "created_at": now,
        }

        # Seed sample items for Tenant A (Pizza Palace)
        self._items["ITEM-101"] = {
            "id": "ITEM-101",
            "tenant_id": "tenant_pizza_palace",
            "name": "Margherita Pizza Large",
            "category": "Food",
            "price": 16.00,
            "stock": 40,
            "created_at": now,
            "updated_at": now,
        }

        # Seed sample items for Tenant B (Sneaker Hub)
        self._items["ITEM-201"] = {
            "id": "ITEM-201",
            "tenant_id": "tenant_sneaker_hub",
            "name": "Air Runner Retro 90",
            "category": "Footwear",
            "price": 140.00,
            "stock": 15,
            "created_at": now,
            "updated_at": now,
        }

    # ---- Tenant Methods ----
    def get_tenant(self, tenant_id: str) -> Optional[dict]:
        return self._tenants.get(tenant_id)

    def create_tenant(self, tenant_record: dict) -> dict:
        self._tenants[tenant_record["id"]] = tenant_record
        return tenant_record

    def update_tenant(self, tenant_id: str, updated_fields: dict) -> Optional[dict]:
        tenant = self._tenants.get(tenant_id)
        if tenant:
            tenant.update(updated_fields)
            return tenant
        return None

    def list_tenants(self) -> List[dict]:
        return list(self._tenants.values())

    # ---- Tenant-Scoped Item Methods (Strict Isolation) ----
    def list_items_for_tenant(self, tenant_id: str) -> List[dict]:
        """Returns ONLY items belonging to the requested tenant."""
        return [item for item in self._items.values() if item["tenant_id"] == tenant_id]

    def get_item_for_tenant(self, item_id: str, tenant_id: str) -> Optional[dict]:
        """Fetches an item ONLY if it belongs to the tenant."""
        item = self._items.get(item_id)
        if item and item["tenant_id"] == tenant_id:
            return item
        return None

    def create_item(self, item_record: dict) -> dict:
        self._items[item_record["id"]] = item_record
        return item_record

    def update_item_for_tenant(self, item_id: str, tenant_id: str, update_dict: dict) -> Optional[dict]:
        item = self.get_item_for_tenant(item_id, tenant_id)
        if not item:
            return None
        item.update(update_dict)
        item["updated_at"] = datetime.utcnow()
        return item

    def delete_item_for_tenant(self, item_id: str, tenant_id: str) -> bool:
        item = self.get_item_for_tenant(item_id, tenant_id)
        if item:
            del self._items[item_id]
            return True
        return False


db = MultiTenantDB()