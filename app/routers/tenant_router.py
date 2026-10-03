"""app/routers/tenant_router.py — Tenant onboarding & subscription management."""

from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.tenant_schema import TenantCreate, TenantResponse, TenantUpgradePlan
from app.services.tenant_service import TenantService
from app.db.tenant_db import db

router = APIRouter(prefix="/tenants", tags=["SaaS Tenant Administration"])


@router.post("", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def register_new_tenant(tenant_in: TenantCreate):
    """Register a new business tenant and provision their isolated workspace."""
    try:
        return TenantService.register_tenant(tenant_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("", response_model=List[TenantResponse])
def list_all_tenants():
    """List all registered tenants on the platform."""
    return db.list_tenants()


@router.put("/{tenant_id}/plan", response_model=TenantResponse)
def upgrade_tenant_plan(tenant_id: str, plan_in: TenantUpgradePlan):
    """Upgrade a tenant's subscription tier (Free -> Pro -> Enterprise)."""
    try:
        updated = TenantService.upgrade_plan(tenant_id, plan_in.new_plan)
        if not updated:
            raise HTTPException(status_code=404, detail="Tenant not found.")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))