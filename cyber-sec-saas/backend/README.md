# Backend (FastAPI)

## Overview
- FastAPI app with async SQLAlchemy
- Prometheus metrics, health endpoints
- JWT auth, RBAC, role dashboards
- WebSocket alert stream
- Hardened for production

## Quick Start
- `pip install -r requirements.txt`
- `uvicorn app.main:app --reload`

## Structure
- `app/` — Main app code
- `scripts/` — DB/init scripts
- `tests/` — Unit tests

## Environment
- Copy `.env.example` to `.env` and set DB/API keys

## Docs
- See root README for full stack info
