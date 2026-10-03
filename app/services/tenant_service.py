"""app/services/tenant_service.py — Business logic for managing SaaS tenants & subscriptions."""

import re
from datetime import datetime
from config import settings
from app.db.tenant_db import db
from app.schemas.tenant_schema import TenantCreate


class TenantService:

    @staticmethod
    def register_tenant(tenant_in: TenantCreate) -> dict:
        # Generate slug-based tenant ID (e.g. "Pizza Palace" -> "tenant_pizza_palace")
        clean_slug = re.sub(r"[^a-zA-Z0-9]+", "_", tenant_in.name.strip().lower()).strip("_")
        tenant_id = f"tenant_{clean_slug}"

        if db.get_tenant(tenant_id):
            raise ValueError(f"Tenant ID '{tenant_id}' already exists.")

        plan_key = tenant_in.plan.lower()
        if plan_key not in settings.PLAN_LIMITS:
            plan_key = "free"

        max_items = settings.PLAN_LIMITS[plan_key]["max_items"]

        record = {
            "id": tenant_id,
            "name": tenant_in.name,
            "admin_email": tenant_in.admin_email,
            "plan": plan_key,
            "max_items_allowed": max_items,
            "is_active": True,
            "created_at": datetime.utcnow(),
        }
        return db.create_tenant(record)

    @staticmethod
    def upgrade_plan(tenant_id: str, new_plan: str) -> dict:
        plan_key = new_plan.lower()
        if plan_key not in settings.PLAN_LIMITS:
            raise ValueError(f"Invalid plan '{new_plan}'. Choose: free, pro, enterprise.")

        max_items = settings.PLAN_LIMITS[plan_key]["max_items"]
        updated = db.update_tenant(tenant_id, {
            "plan": plan_key,
            "max_items_allowed": max_items
        })
        return updated