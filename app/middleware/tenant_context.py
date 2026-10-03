"""
app/middleware/tenant_context.py — FastAPI Dependency for Tenant Isolation.

Extracts the `X-Tenant-ID` header from incoming requests, validates the tenant,
and injects the tenant context into the router endpoints.
"""

from fastapi import Header, HTTPException, status
from app.db.tenant_db import db


def get_current_tenant(
    x_tenant_id: str = Header(
        ...,
        alias="X-Tenant-ID",
        description="Tenant Identifier (e.g. tenant_pizza_palace, tenant_sneaker_hub)",
        example="tenant_pizza_palace"
    )
) -> dict:
    """
    FastAPI Dependency:
    1. Reads `X-Tenant-ID` header.
    2. Validates tenant existence in the database.
    3. Checks if the tenant account is active.
    4. Injects tenant dictionary into the endpoint.
    """
    if not x_tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required header: 'X-Tenant-ID'"
        )

    tenant = db.get_tenant(x_tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant '{x_tenant_id}' does not exist."
        )

    if not tenant.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Tenant account '{x_tenant_id}' is suspended or inactive."
        )

    return tenant