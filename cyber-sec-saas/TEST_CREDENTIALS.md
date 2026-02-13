# 🔐 Enterprise Test User Credentials

## ✅ Current Status: 9 Test Users Created Successfully

Database: SQLite (cybersec.db)  
Backend: Running on http://localhost:8000  
Frontend: http://localhost:5175  
Last Updated: February 11, 2026

---

## 🚀 Login Portal

**URL:** http://localhost:5175/portal/login

All passwords follow pattern: `{Role}@2026!` (updated for 2026)

---

## 8-Role Enterprise System

### 🔴 SUPER ADMIN - Full Platform Control
- **Email:** `superadmin@cybersecurity.io`
- **Password:** `Super@2026!`
- **Backend Role:** `SuperAdmin`
- **Dashboard:** Super Administrator Dashboard
- **Capabilities:**
  - Create/manage users
  - Assign roles
  - View all data
  - System configuration
  - Audit logs
  - 24 permissions (all resources)

---

### 🟠 SECURITY ADMIN - Security Operations
- **Email:** `sec.admin@cybersecurity.io`
- **Password:** `SecAdmin@2026!`
- **Backend Role:** `SecurityAdmin`
- **Dashboard:** Security Operations Dashboard
- **Capabilities:**
  - Manage alerts
  - Create incidents
  - View threats
  - Security automation
  - 14 permissions

---

### 🟡 SOC ANALYST - Threat Monitoring
- **Email:** `soc.analyst@cybersecurity.io`
- **Password:** `SOC@2026!`
- **Backend Role:** `SOCAnalyst`
- **Dashboard:** SOC Analyst Dashboard (with queue)
- **Also Available:**
  - `soc2.analyst@cybersecurity.io` / `SOC@2026!` (Alice Johnson)
- **Capabilities:**
  - Monitor alerts
  - Respond to incidents
  - View threat intel
  - 9 permissions

---

### 🔵 INFRASTRUCTURE ADMIN - Infrastructure Monitoring
- **Email:** `infra.admin@cybersecurity.io`
- **Password:** `Infra@2026!`
- **Backend Role:** `InfraAdmin`
- **Dashboard:** Infrastructure Dashboard
- **Capabilities:**
  - Monitor uptime
  - View CPU/Memory metrics
  - Cloud status
  - 5 permissions

---

### 🟣 COMPLIANCE OFFICER - Audit & Compliance
- **Email:** `compliance@cybersecurity.io`
- **Password:** `Compliance@2026!`
- **Backend Role:** `ComplianceOfficer`
- **Dashboard:** Compliance Dashboard
- **Capabilities:**
  - View compliance reports
  - Access audit logs
  - Risk assessment
  - 5 permissions

---

### ⚪ AUDITOR - Read-Only Audit
- **Email:** `auditor@cybersecurity.io`
- **Password:** `Audit@2026!`
- **Backend Role:** `Auditor`
- **Dashboard:** Audit Log Dashboard (read-only)
- **Capabilities:**
  - View audit logs
  - Export audit data
  - 5 permissions (read-only)

---

### ⚫ INTERNAL USER - Limited Internal Access
- **Email:** `internal.user@cybersecurity.io`
- **Password:** `User@2026!`
- **Backend Role:** `InternalUser`
- **Dashboard:** Internal Metrics Dashboard
- **Capabilities:**
  - View internal metrics
  - Limited dashboard access
  - 2 permissions

---

### 👥 HYBRID ADMIN - Multi-Role User (Testing)
- **Email:** `hybrid.admin@cybersecurity.io`
- **Password:** `Hybrid@2026!`
- **Backend Roles:** `SecurityAdmin` + `InfraAdmin`
- **Dashboard:** Combined Security + Infrastructure
- **Capabilities:**
  - Both SecurityAdmin and InfraAdmin permissions
  - Test multi-role dashboard switching

---

## Dashboard Config API

### Endpoints

```
GET /api/internal/dashboard/config
  → Get dashboard for current user

GET /api/internal/dashboard/config/{role_type}
  → Get dashboard for specific role (admin only)

GET /api/internal/dashboard/config/all
  → Get all dashboards (admin only)

GET /api/internal/dashboard/stats
  → Get dashboard statistics
```

### Example Response

```json
{
  "role_type": "SuperAdmin",
  "display_name": "Super Administrator",
  "menu_items": [
    {
      "id": "dashboard",
      "label": "Dashboard",
      "icon": "grid-3x3-gap",
      "path": "/dashboard"
    }
  ],
  "widgets": [
    {
      "id": "active_alerts",
      "type": "metric_card",
      "title": "Active Alerts",
      "grid_x": 0,
      "grid_y": 0,
      "grid_width": 2,
      "grid_height": 2
    }
  ],
  "permissions": ["user:create", "user:read", ...],
  "quick_actions": [...]
}
```

---

## Testing Workflow

### 1. Test Each User Role
```
Login with each credential above
Verify redirect to correct dashboard
Check role-specific widgets visible
```

### 2. Test Multi-Role User
```
Login as hybrid.admin@cybersecurity.io
Should show SecurityAdmin + InfraAdmin features
```

### 3. Test Dashboard API
```
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/internal/dashboard/config
```

### 4. Test Permission Enforcement
```
Login as SOCAnalyst (9 permissions)
Try to access admin features (should fail)
Login as SuperAdmin (30 permissions)
Should access all features
```

---

## Backend Endpoints

### Authentication
```
POST /auth/login
POST /auth/refresh  
POST /auth/logout
GET  /auth/me
GET  /auth/roles
```

### Dashboard
```
GET  /api/internal/dashboard/config
GET  /api/internal/dashboard/config/{role_type}
GET  /api/internal/dashboard/config/all
GET  /api/internal/dashboard/stats
```

### Health
```
GET  /health
```

---

## Database Schema

**11 Production Tables:**
- users (UUID PK, multi-role support)
- roles (8 predefined roles)
- user_roles (many-to-many association)
- audit_logs (comprehensive audit trail)
- alerts, incidents, threat_intel_records
- cloud_status_records, uptime_records
- system_metrics, risk_scores

---

## Troubleshooting

### Login Error: "Objects are not valid as a React child"
**Cause:** Frontend trying to render validation error object  
**Solution:** Check browser console for error details, ensure email format is valid (e.g., `user@cybersecurity.io`)

### 401 Unauthorized
**Cause:** Token expired or invalid credentials  
**Solution:** 
1. Clear browser localStorage
2. Verify credentials match test users above
3. Check backend is running on port 8000

### "User has no assigned roles"
**Cause:** User exists but has no roles  
**Solution:** Re-run seed script: `python scripts/seed_enterprise_users.py`

### Dashboard returns empty widgets
**Cause:** Role type not found in dashboard service  
**Solution:** Use exact role type: `SuperAdmin`, `SecurityAdmin`, `SOCAnalyst`, `InfraAdmin`, `ComplianceOfficer`, `Auditor`, `InternalUser`, or `PublicVisitor`

---

## Production Security Note

⚠️ **These are TEST credentials only!**

Never use in production:
1. Delete all test users
2. Use strong passwords (minimum 16 chars)
3. Enable MFA
4. Rotate JWT secrets  
5. Use HTTPS only
6. Implement rate limiting (already configured)

---

**Created:** February 11, 2026  
**System:** Enterprise Cyber Intelligence Platform v2.0  
**Roles:** 8 (SuperAdmin, SecurityAdmin, SOCAnalyst, InfraAdmin, ComplianceOfficer, Auditor, InternalUser, PublicVisitor)  
**Users:** 9 test accounts across all roles
