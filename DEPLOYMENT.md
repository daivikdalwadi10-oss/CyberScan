# Vercel Deployment Guide

## 1. Frontend
- Ensure `cyber-sec-saas/frontend` is production-ready.
- Vercel will use `@vercel/static-build` for React/Vite.

## 2. Backend
- FastAPI backend entry: `cyber-sec-saas/backend/app/main.py`.
- Vercel uses `@vercel/python` for Python API routes.

## 3. Configuration
- `vercel.json` is set up for routing and builds.
- API routes: `/api/*` → backend.
- Static routes: `/*` → frontend.

## 4. Environment Variables
- Set `.env` values in Vercel dashboard for backend.

## 5. Deploy Steps
1. Push this repo to GitHub.
2. Import project in Vercel.
3. Set build output for frontend: `cyber-sec-saas/frontend/dist`.
4. Set Python entry for backend: `cyber-sec-saas/backend/app/main.py`.
5. Add environment variables.
6. Deploy and verify.

## 6. Troubleshooting
- Check Vercel logs for build/runtime errors.
- Ensure all dependencies are in `requirements.txt` and `package.json`.

---
For advanced routing, see [vercel.json](vercel.json).
