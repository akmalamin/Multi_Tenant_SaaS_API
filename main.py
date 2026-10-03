"""
main.py — Multi-Tenant SaaS Engine Entry Point.
Run: uvicorn main:app --reload --port 8000
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from app.routers import health_router, tenant_router, item_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url=settings.DOCS_URL
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Register routers
app.include_router(health_router.router)
app.include_router(tenant_router.router, prefix=settings.API_V1_STR)
app.include_router(item_router.router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs": f"http://localhost:8000{settings.DOCS_URL}",
        "pre_seeded_tenants": [
            {"id": "tenant_pizza_palace", "plan": "free", "max_items": 5},
            {"id": "tenant_sneaker_hub", "plan": "pro", "max_items": 100}
        ]
    }


if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════════════════════════╗
║   🏢 MULTI-TENANT SAAS BACKEND — Day 128                ║
║   Interactive Swagger Docs: http://localhost:8000/docs   ║
╚══════════════════════════════════════════════════════════╝
    """)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)