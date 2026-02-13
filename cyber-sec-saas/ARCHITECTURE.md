# 🏢 Enterprise Architecture

## SentinelScope - Dual-Portal Security Operations Platform

**Version:** 2.0  
**Architecture Type:** Enterprise Internal + Public Transparency

---

## 🎯 System Overview

SentinelScope is an **Enterprise Internal Cybersecurity & Monitoring Platform** with a **Public Transparency Dashboard**. The system is split into two distinct experiences:

1. **Public Transparency Portal** - No authentication, transparency-oriented
2. **Company Internal Portal** - Secure authentication, full operations

### Key Characteristics

- ✅ **No Billing/Pricing** - Pure enterprise internal tool
- ✅ **Dual Experience** - Public trust dashboard + secure operations portal
- ✅ **Role-Based Access** - 7 distinct internal roles with granular permissions
- ✅ **Transparency First** - Public can view aggregated security posture
- ✅ **Zero Trust** - All sensitive operations require authentication

---

## 🌍 Public Transparency Portal

### Purpose
Build trust and demonstrate security commitment through transparency.

### Routes
- `/` - Landing page with trust metrics
- `/status` - Live system status dashboard
- `/public-reports` - Published security audit reports

### Access
- ✅ **No login required**
- ✅ **Anyone can view**
- ✅ **Mobile-optimized**

### Data Shown
- System operational status (live)
- Aggregated risk score (non-sensitive)
- Uptime percentage (30-day rolling)
- Resolved incidents count
- Compliance framework status (SOC2, ISO 27001, GDPR, HIPAA)
- Service health (Web, API, DB, Auth, Monitoring)
- Published audit reports (sanitized)
- Recent security updates timeline

### Data NOT Shown
- ❌ Internal vulnerabilities
- ❌ Detailed security logs
- ❌ User information
- ❌ Internal alerts
- ❌ API keys or credentials
- ❌ Tenant-specific data
- ❌ Exploit details

### Design
- Clean, minimal layout
- No sidebar navigation
- Large trust indicators
- Animated uptime circle
- Compliance badges
- Professional, trust-oriented aesthetic
- Glassmorphism with reduced complexity

---

## 🔐 Company Internal Portal

### Purpose
Full security operations platform for authorized internal teams.

### Routes
- `/portal/login` - Secure authentication
- `/portal/dashboard/{role}` - Role-specific dashboards
- `/portal/users` - User management
- `/portal/projects` - Security projects/targets
- `/portal/reports` - Internal reports with full data

### Access
- 🔒 **Login required**
- 🔒 **JWT authentication**
- 🔒 **Role-based authorization**
- 🔒 **Tenant isolation**

### Roles & Dashboards

#### 1. SuperAdmin
**Path:** `/portal/dashboard/super-admin`

**Responsibilities:**
- Platform-wide operations
- Tenant management (create/list)
- System performance monitoring
- Global security metrics

**Permissions:**
- Full platform access
- Create tenants
- View all tenant data
- Manage global settings

#### 2. TenantAdmin
**Path:** `/portal/dashboard/tenant-admin`

**Responsibilities:**
- Organization administration
- User management
- Project oversight
- API key management

**Permissions:**
- Manage users in tenant
- Create/edit projects
- View all tenant scans
- Export reports
- Manage user roles

#### 3. SecurityManager
**Path:** `/portal/dashboard/manager`

**Responsibilities:**
- Risk trend analysis
- Scan approval workflows
- Analyst assignment
- Compliance oversight

**Permissions:**
- View all scans
- Approve/reject scans
- Assign analysts
- Access compliance dashboard
- Export reports

#### 4. SecurityAnalyst
**Path:** `/portal/dashboard/analyst`

**Responsibilities:**
- Execute security scans
- Analyze vulnerabilities
- Document remediation steps
- Track finding resolution

**Permissions:**
- Run scans
- Edit vulnerability details
- Add remediation notes
- Mark findings as resolved
- Create project targets

#### 5. SOCOperator
**Path:** `/portal/dashboard/soc`

**Responsibilities:**
- Real-time alert monitoring
- Incident management
- Escalation handling
- MTTR tracking

**Permissions:**
- View live alerts
- Escalate incidents
- Update incident status
- View real-time dashboards

#### 6. Auditor
**Path:** `/portal/dashboard/auditor`

**Responsibilities:**
- Compliance reporting
- Audit log review
- Evidence collection
- Report generation

**Permissions:**
- View all audit logs (read-only)
- Export compliance reports
- Download evidence packages
- View scan history

#### 7. Viewer
**Path:** `/portal/dashboard/viewer`

**Responsibilities:**
- Read-only stakeholder access
- Report viewing
- Risk awareness

**Permissions:**
- View dashboards (read-only)
- Download published reports
- View aggregated metrics
- No edit capabilities

### Design
- Full glassmorphism UI
- Dynamic sidebar navigation
- Role-aware menu items
- Enterprise-grade polish
- Dark cyber theme with neon accents

---

## 🔌 API Architecture

### Public Endpoints (`/public/*`)

**No authentication required**

#### `GET /public/status`
Returns aggregated system health:
- System status (operational/degraded/down)
- Risk score (aggregated, 0-100)
- Uptime percentage
- Incidents resolved count
- Service health per component
- Compliance status
- Recent updates

**Security:** Returns only aggregated, non-sensitive data.

#### `GET /public/reports`
Returns published security reports:
- Report title, type, date
- Sanitized summaries
- Redacted findings
- Publication status

**Security:** Internal vulnerability details removed.

---

### Internal Endpoints (`/auth/*`, `/users/*`, etc.)

**JWT Authentication Required**

#### Authentication
- `POST /auth/login` - JWT token issuance
- Role and tenant extracted from token

#### Protected Resources
- `GET /users` - List tenant users (TenantAdmin+)
- `POST /projects` - Create security project (Analyst+)
- `GET /scans` - List scans (all roles)
- `POST /scan/{project_id}` - Execute scan (Analyst+)
- `GET /report/{scan_id}` - Download full report (Analyst+)
- `POST /tenants` - Create tenant (SuperAdmin only)
- `GET /tenants` - List tenants (SuperAdmin only)

**Security:** All endpoints validate JWT, role, and tenant_id.

---

## 🎨 UI Design System

### Public Portal Theme
- **Palette:** Cleaner, more minimal
- **Accent:** Same teal (#00f5d4) but softer usage
- **Layout:** No sidebar, simple top nav
- **Cards:** Larger, more spacious
- **Animations:** Subtle, professional
- **Typography:** Clear, trust-building
- **Goal:** Credibility and transparency

### Company Portal Theme
- **Palette:** Full cyber dark mode
- **Accent:** Bright teal (#00f5d4) with glow effects
- **Layout:** Sidebar navigation
- **Cards:** Glassmorphism with high opacity
- **Animations:** Smooth framer-motion transitions
- **Typography:** Grotesk, technical
- **Goal:** Enterprise operations efficiency

### Shared Components
- GlassCard
- Button (primary/secondary variants)
- Input fields with cyber styling
- Charts (Recharts with accent colors)
- Icons (Lucide React)

---

## 🔐 Security Model

### Authentication Flow

```
1. User visits /portal/login
2. Enters credentials
3. Backend validates against User table
4. Returns JWT with claims: { sub: user_id, role: "TenantAdmin", tenant_id: 123 }
5. Frontend stores token in localStorage
6. Frontend decodes JWT to extract role and tenant
7. Routes to appropriate dashboard: /portal/dashboard/tenant-admin
8. All API calls include Authorization: Bearer {token}
9. Backend validates token + role + tenant on every request
```

### Authorization Layers

**Layer 1: Frontend Routing**
- ProtectedRoute component checks session
- Redirects to /portal/login if no token
- Checks allowedRoles prop
- Redirects to forbidden page if role mismatch

**Layer 2: Backend Validation**
- JWT signature verification
- Role extraction from token claims
- Tenant isolation (filters DB queries by tenant_id)
- Permission decorators (@require_roles)

**Layer 3: Data Isolation**
- All queries scoped to user's tenant_id
- SuperAdmin can override scope
- Audit log records all access

### Public Data Safeguards
- `/public/*` endpoints use separate logic
- Aggregate-only calculations
- No JOIN queries with sensitive tables
- Redacted report content
- Rate limiting (100 req/min)

---

## 📊 Data Flow Examples

### Public Status Dashboard
```
Frontend (/status) 
  → GET /public/status (no auth)
  → Backend aggregates scan risk_scores
  → Returns { riskScore: 32, uptime: 99.98, ... }
  → Frontend displays in glassmorphism cards
```

### Internal Scan Execution
```
Analyst Dashboard (/portal/dashboard/analyst)
  → Click "Run Scan" on project
  → POST /scan/{project_id} + JWT token
  → Backend validates JWT → extracts role (SecurityAnalyst) + tenant_id
  → Creates Scan record with tenant_id
  → Scanner engine executes
  → Returns scan_id
  → Frontend polls GET /scan/{scan_id} for updates
  → Displays vulnerabilities in table
```

### SuperAdmin Tenant Creation
```
SuperAdmin Dashboard (/portal/dashboard/super-admin)
  → Fill "Create Tenant" form → name: "Acme Corp"
  → POST /tenants { "name": "Acme Corp" } + JWT token
  → Backend validates role === SuperAdmin
  → Creates Tenant record
  → Returns tenant_id
  → Frontend adds to tenant list
```

---

## 🗄️ Database Schema

### Core Tables
- **tenants** - Organizations (multi-tenant isolation)
- **users** - Internal staff with roles
- **projects** - Security scan targets
- **scans** - Vulnerability scan executions
- **vulnerabilities** - Individual findings
- **audit_logs** - All user actions

### Public Data Queries
```sql
-- Public status uses aggregate functions only
SELECT AVG(risk_score) as avg_risk 
FROM scans 
WHERE status = 'completed' 
AND created_at >= NOW() - INTERVAL '30 days';

-- NO direct vulnerability or user queries
```

### Internal Data Queries
```sql
-- Internal queries filter by tenant_id
SELECT * FROM scans 
WHERE tenant_id = <user_tenant_id>
ORDER BY created_at DESC;

-- SuperAdmin bypasses tenant filter
SELECT * FROM scans 
ORDER BY created_at DESC;
```

---

## 🚀 Deployment Architecture

### Frontend (Vite + React)
- **Public Routes:** Static hosting (Vercel/Netlify)
- **Build:** `npm run build` → dist/
- **Env:** `VITE_API_URL` → backend URL

### Backend (FastAPI + PostgreSQL)
- **Public Endpoints:** No rate limit bypass needed
- **Internal Endpoints:** JWT validation middleware
- **Database:** PostgreSQL with row-level tenant_id filters
- **Migrations:** Alembic for schema changes

### Recommended Stack
- **Frontend:** Vercel (auto HTTPS, CDN, preview deploys)
- **Backend:** Railway/Render (auto-scaling, PostgreSQL addon)
- **Database:** Managed PostgreSQL (Neon/Supabase)
- **Monitoring:** Sentry (errors) + Uptime monitoring service

---

## 📈 Scaling Considerations

### Public Portal
- **Caching:** Cache `/public/status` for 60 seconds (Redis)
- **CDN:** Static assets on Cloudflare
- **Rate Limiting:** 100 requests/min per IP

### Company Portal
- **Database:** Connection pooling (SQLAlchemy engine)
- **API:** Horizontal scaling (multiple Gunicorn workers)
- **Background Jobs:** Celery for scan execution (async)

---

## 🧪 Testing Strategy

### Public Portal Tests
- ✅ Endpoint returns 200 without auth
- ✅ No sensitive data in response
- ✅ Rate limit enforced
- ✅ Aggregation math correct

### Company Portal Tests
- ✅ Unauthorized requests rejected (401)
- ✅ Wrong role blocked (403)
- ✅ Tenant isolation verified
- ✅ JWT expiration handled
- ✅ Audit log created per action

---

## 📝 Migration Checklist

From SaaS to Enterprise model:

- ✅ Remove billing/pricing pages
- ✅ Remove public registration (/auth/register for tenants)
- ✅ Split routes: `/` public vs `/portal` internal
- ✅ Create `/public/*` API endpoints
- ✅ Update sidebar to use `/portal` paths
- ✅ Remove "Start free" CTAs → "View Status"
- ✅ Update landing page messaging (no SaaS copy)
- ✅ Add public transparency dashboard
- ✅ Sanitize public report content
- ✅ Document dual-portal architecture

---

## 🔗 Quick Reference

| Portal | Base Path | Auth | Purpose |
|--------|-----------|------|---------|
| Public | `/` | No | Transparency & trust |
| Company | `/portal` | Yes | Operations & administration |

| Role | Path | Key Actions |
|------|------|-------------|
| SuperAdmin | `/portal/dashboard/super-admin` | Create tenants, global view |
| TenantAdmin | `/portal/dashboard/tenant-admin` | Manage users, projects |
| SecurityManager | `/portal/dashboard/manager` | Approve scans, assign analysts |
| SecurityAnalyst | `/portal/dashboard/analyst` | Run scans, analyze findings |
| SOCOperator | `/portal/dashboard/soc` | Monitor alerts, escalate |
| Auditor | `/portal/dashboard/auditor` | Review logs, export reports |
| Viewer | `/portal/dashboard/viewer` | Read-only access |

---

**Last Updated:** February 11, 2026  
**Architecture Version:** 2.0 - Enterprise Dual-Portal
