"""app/schemas/tenant_schema.py — Pydantic models for Tenant provisioning."""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class TenantCreate(BaseModel):
    name: str = Field(..., min_length=2, example="Pizza Palace Corp")
    admin_email: EmailStr = Field(..., example="owner@pizzapalace.com")
    plan: str = Field(default="free", example="free", description="Subscription plan: free, pro, enterprise")


class TenantResponse(BaseModel):
    id: str = Field(..., example="tenant_pizza_palace")
    name: str
    admin_email: str
    plan: str
    max_items_allowed: int
    is_active: bool
    created_at: datetime


class TenantUpgradePlan(BaseModel):
    new_plan: str = Field(..., example="pro", description="New plan tier: pro or enterprise")