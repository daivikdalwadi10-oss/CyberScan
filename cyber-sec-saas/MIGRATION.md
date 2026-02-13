# 🔄 Migration Guide: v1.0 (SaaS) → v2.0 (Enterprise Dual-Portal)

## Overview

SentinelScope has been restructured from a **SaaS platform** to an **Enterprise Internal Platform** with a **Public Transparency Dashboard**.

---

## Breaking Changes

### Routes

#### Frontend Routes Changed

| Old Route (v1.0) | New Route (v2.0) | Access |
|------------------|------------------|--------|
| `/` | `/` | Public (landing page with trust metrics) |
| `/auth/login` | `/portal/login` | Public (company portal login) |
| `/auth/register` | *Removed* | Registration disabled (internal tool) |
| `/app/super-admin` | `/portal/dashboard/super-admin` | Auth required |
| `/app/tenant-admin` | `/portal/dashboard/tenant-admin` | Auth required |
| `/app/manager` | `/portal/dashboard/manager` | Auth required |
| `/app/analyst` | `/portal/dashboard/analyst` | Auth required |
| `/app/soc` | `/portal/dashboard/soc` | Auth required |
| `/app/auditor` | `/portal/dashboard/auditor` | Auth required |
| `/app/viewer` | `/portal/dashboard/viewer` | Auth required |
| `/app/users` | `/portal/users` | Auth required |
| `/app/projects` | `/portal/projects` | Auth  required |
| `/app/reports` | `/portal/reports` | Auth required |
| *New* | `/status` | Public (live status dashboard) |
| *New* | `/public-reports` | Public (sanitized reports) |

#### Backend Routes Changed

| Old Route (v1.0) | New Route (v2.0) | Auth Required |
|------------------|------------------|---------------|
| All routes | *Unchanged* | ✅ Yes |
| *New* | `GET /public/status` | ❌ No |
| *New* | `GET /public/reports` | ❌ No |

### Component Imports

If you have custom code importing components:

```jsx
// OLD (v1.0)
import Landing from "./pages/Landing/index.jsx";
import Login from "./pages/Auth/Login.jsx";

// NEW (v2.0)
import PublicLanding from "./pages/PublicPortal/Landing/index.jsx";
import CompanyLogin from "./pages/CompanyPortal/Auth/Login.jsx";
```

### Role Constants

Role names now use SCREAMING_SNAKE_CASE:

```js
// OLD (v1.0)
ROLES.superAdmin
ROLES.tenantAdmin
ROLES.securityManager
ROLES.securityAnalyst
ROLES.socOperator
ROLES.auditor
ROLES.viewer

// NEW (v2.0)
ROLES.SUPER_ADMIN
ROLES.TENANT_ADMIN
ROLES.SECURITY_MANAGER
ROLES.SECURITY_ANALYST
ROLES.SOC_OPERATOR
ROLES.AUDITOR
ROLES.VIEWER
```

---

## New Features

### Public Transparency Portal

**New Pages:**
1. **Public Landing (`/`)** - Trust-oriented homepage with features and metrics
2. **Live Status Dashboard (`/status`)** - Real-time operational health
3. **Public Reports (`/public-reports`)** - Sanitized security audit summaries

**New API Endpoints:**
- `GET /public/status` - Aggregated system metrics (no auth)
- `GET /public/reports` - Published reports list (no auth)

**What's Public:**
- System operational status
- Aggregated risk score (0-100)
- Uptime percentage
- Resolved incidents count
- Compliance framework status
- Service health per component

**What's NOT Public:**
- Internal vulnerabilities
- User data
- Detailed logs
- API keys
- Tenant-specific information
- Exploit details

### Company Internal Portal

**Login moved to:** `/portal/login`

**All company features require authentication now via separate portal path.**

---

## Removed Features

### Billing/Pricing
- ❌ No billing pages
- ❌ No pricing tiers
- ❌ No payment processing
- ✅ Pure enterprise internal tool

### Public Registration
- ❌ `/auth/register` removed from public access
- ✅ User accounts created by TenantAdmin via portal
- ✅ SuperAdmin created via seed script only

---

## Migration Steps

### For Developers

1. **Update bookmarks:**
   - Old: `http://localhost:5173/app/analyst`
   - New: `http://localhost:5173/portal/dashboard/analyst`

2. **Update any hardcoded routes** in custom code to use `/portal` prefix

3. **Clear localStorage** to reset authentication state:
   ```js
   localStorage.clear();
   ```

4. **Re-login** via `/portal/login`

### For Backend

1. **Pull latest code**

2. **No database migration needed** - schema unchanged

3. **Restart backend server:**
   ```powershell
   uvicorn app.main:app --reload
   ```

4. **Verify public endpoints:**
   ```powershell
   curl http://localhost:8000/public/status
   curl http://localhost:8000/public/reports
   ```

### For Frontend

1. **Pull latest code**

2. **Install any new dependencies** (none in this release)

3. **Restart dev server:**
   ```bash
   npm run dev
   ```

4. **Test both portals:**
   - Visit http://localhost:5173/ (public)
   - Visit http://localhost:5173/status (public)
   - Visit http://localhost:5173/portal/login (company)

---

## Backward Compatibility

### Broken

- ❌ Old `/app/*` routes will 404
- ❌ Old `/auth/login` will 404 (use `/portal/login`)
- ❌ Role constants changed (lowercase → UPPERCASE)

### Still Works

- ✅ All API endpoints (except new `/public/*`)
- ✅ JWT authentication flow
- ✅ Database schema
- ✅ All backend business logic
- ✅ Existing user accounts

---

## Testing Checklist

After migration, verify:

- [ ] Public landing page loads at `/`
- [ ] Public status dashboard loads at `/status`
- [ ] Public reports page loads at `/public-reports`
- [ ] `GET /public/status` returns 200 without auth
- [ ] `GET /public/reports` returns 200 without auth
- [ ] Company login works at `/portal/login`
- [ ] Dashboards load at `/portal/dashboard/{role}`
- [ ] Sidebar navigation uses `/portal` paths
- [ ] Protected routes require authentication
- [ ] Role-based access control still enforced
- [ ] Tenant isolation still working

---

## Architecture Differences

| Aspect | v1.0 (SaaS) | v2.0 (Enterprise) |
|--------|-------------|-------------------|
| Model | Multi-tenant SaaS | Internal Corporate Tool |
| Public Access | Marketing landing only | Full status dashboard |
| Registration | Public signup | Admin-created accounts only |
| Billing | Stripe integration | No billing |
| Routes | `/app/*` | `/portal/*` |
| Public Data | None | Aggregated metrics |

---

## Documentation

**New Files:**
- `ARCHITECTURE.md` - Comprehensive dual-portal architecture guide
- `MIGRATION.md` - This document

**Updated Files:**
- `README.md` - Reflects new dual-portal model
- `STATUS.md` - Updated completion status

---

## Support

**Questions?**
- Read `ARCHITECTURE.md` for complete system design
- Check `README.md` for quick start guide
- Review `STATUS.md` for current project state

**Found a bug?**
- Check that routes use `/portal` prefix for company portal
- Verify role constants use UPPERCASE format
- Ensure public pages don't require authentication

---

**Migration Completed:** February 11, 2026  
**Architecture Version:** 2.0 - Enterprise Dual-Portal
