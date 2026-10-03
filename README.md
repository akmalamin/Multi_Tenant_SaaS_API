# 🏢 Multi-Tenant SaaS Backend Architecture (FastAPI)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)]()
[![Framework: FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

A production-grade multi-tenant B2B SaaS architecture built with **FastAPI** and **Pydantic**. Demonstrates strict tenant data isolation, dynamic `X-Tenant-ID` header extraction, tenant-scoped inventory management, and automated subscription tier quota enforcement (Free vs Pro).

---

## 🌟 Key Capabilities

- **🛡️ 100% Data Isolation:** Queries are strictly bounded to the requesting tenant.
- **🎛️ Header-Based Context Extraction:** Automatically validates incoming `X-Tenant-ID` headers.
- **💳 Plan Quota Enforcement:** Rejects item creation when a Free Tier tenant exceeds their 5-item limit (`402 Payment Required`).
- **🔄 Dynamic Plan Upgrades:** 1-click subscription tier upgrades unlock expanded limits on the fly.

---

## 🚀 Quick Start

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000