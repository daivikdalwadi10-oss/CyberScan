# SentinelScope - Enterprise Security Operations Platform

🏢 **Enterprise Internal Cybersecurity & Monitoring Platform** with Public Transparency Dashboard

## 🎯 What Is This?

SentinelScope is a **dual-portal security platform** designed for enterprise internal use:

1. **Public Transparency Portal** (`/`) - No login required
   - Live system status dashboard
   - Aggregated security posture metrics
   - Published audit reports (sanitized)
   - Build trust through transparency

2. **Company Internal Portal** (`/portal`) - Secure authentication required
   - 7 role-specific dashboards
   - Full security operations workflow
   - Vulnerability management
   - Compliance reporting

**Key Characteristics:**
- ✅ No billing/pricing - pure internal tool
- ✅ Public can view aggregated security metrics
- ✅ Internal teams access full operational data
- ✅ Role-based access control (SuperAdmin, TenantAdmin, SecurityManager, SecurityAnalyst, SOCOperator, Auditor, Viewer)
- ✅ Multi-tenant architecture with complete data isolation

## 🚀 Quick Start

### Prerequisites
- Python 3.14+ (or 3.11+)
- Node.js 18+ 
- PostgreSQL 15+

### Backend Setup

1. **Install dependencies:**
```powershell
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

2. **Configure environment:**
```powershell
# Copy .env.example to .env and update values
copy .env.example .env
# Update DATABASE_URL and JWT_SECRET
```

3. **Run database migrations:**
```powershell
alembic upgrade head
```

4. **Seed SuperAdmin (optional but recommended):**
```powershell
$env:SUPER_ADMIN_EMAIL = "admin@platform.local"
$env:SUPER_ADMIN_PASSWORD = "change-me-now"
$env:SUPER_ADMIN_TENANT = "Platform"
$env:PYTHONPATH = "."
python scripts/seed_super_admin.py
```

5. **Start backend server:**
```powershell
uvicorn app.main:app --reload
```
Server runs at http://localhost:8000

### Frontend Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Start dev server:**
```bash
npm run dev
```
App runs at http://localhost:5173 (or 5174 if 5173 is busy)

## 🧪 Running Tests

### Backend Tests
```powershell
cd backend
pytest -v
```
**Current Status:** ✅ 2/2 tests passing

### Frontend Tests
```bash
cd frontend  
npm run test -- --run
```
**Current Status:** ✅ 1/1 test passing

## 📚 Documentation

- [STATUS.md](STATUS.md) - Detailed project status and next steps
- [API Documentation](http://localhost:8000/docs) - FastAPI auto-generated docs (when server running)

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- React 18.3.1 with React Router 6.26.2
- Vite 7.3.1 for build tooling
- TailwindCSS 3.4.14 for styling
- Framer Motion 11.4.0 for animations
- Recharts 2.12.7 for data visualization
- Vitest 2.1.9 + Testing Library for tests

**Backend:**
- FastAPI 0.115.8
- SQLAlchemy 2.0.36 ORM
- Alembic 1.13.2 for migrations
- Psycopg 3.2.9 (PostgreSQL adapter)
- Pydantic 2.x for validation
- python-jose for JWT
- pytest 8.2.2 for tests

**Database:**
- PostgreSQL 15+ (Neon hosted or local)

### Project Structure
```
cyber-sec-saas/
├── backend/
│   ├── app/
│   │   ├── auth/          # JWT, password hashing, dependencies
│   │   ├── models/        # SQLAlchemy models
│   │   ├── routes/        # API endpoints
│   │   ├── scanner/       # Vulnerability scanning engine
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── utils/         # Helpers (logging, rate limit, risk)
│   ├── alembic/           # Database migrations
│   ├── scripts/           # Utility scripts (seed, etc)
│   └── tests/             # pytest test suite
├── frontend/
│   └── src/
│       ├── components/    # Reusable UI components
│       ├── context/       # React context (auth)
│       ├── pages/         # Page components
│       │   ├── Auth/      # Login, Register
│       │   ├── Dashboard/ # Role-specific dashboards
│       │   └── Landing/   # Marketing landing page
│       ├── router/        # React Router config
│       ├── services/      # API client
│       ├── utils/         # Helpers (JWT decode, permissions)
│       └── __tests__/     # Vitest test suite
└── README.md
```

## 🎭 User Roles

The platform supports 7 distinct roles with tailored dashboards:

1. **SuperAdmin** - Platform administration, tenant management  
  Dashboard: `/portal/dashboard/super-admin`

2. **TenantAdmin** - Organizational administration  
  Dashboard: `/portal/dashboard/tenant-admin`

3. **SecurityManager** - Approval workflows, team oversight  
   Dashboard: `/portal/dashboard/manager`

4. **SecurityAnalyst** - Vulnerability analysis, remediation  
   Dashboard: `/portal/dashboard/analyst`

5. **SOCOperator** - Real-time monitoring, incident response  
   Dashboard: `/portal/dashboard/soc`

6. **Auditor** - Compliance reporting, audit logs  
   Dashboard: `/portal/dashboard/auditor`

7. **Viewer** - Read-only stakeholder access  
   Dashboard: `/portal/dashboard/viewer`

## 🌍 Dual Portal Architecture

### Public Transparency Portal (No Auth Required)

**Routes:**
- `/` - Landing page with trust metrics and features
- `/status` - Live system status dashboard
- `/public-reports` - Published security audit reports

**Purpose:** Build trust through transparency. Show aggregated security posture without exposing sensitive details.

**Data Shown:**
- System operational status (live)
- Aggregated risk score
- Uptime percentage (30-day rolling)
- Resolved incidents count
- Compliance framework status
- Published audit summaries

**Data NOT Shown:**
- Internal vulnerabilities
- User information
- Detailed logs
- API keys
- Tenant-specific data

### Company Internal Portal (Auth Required)

**Login:** `/portal/login`  
**Dashboard Routes:** `/portal/dashboard/{role}`  
**Shared Pages:** `/portal/users`, `/portal/projects`, `/portal/reports`

**Purpose:** Full security operations for authorized internal teams.

**Access:** Requires JWT authentication with role-based authorization.

## 🌐 Key Features

### Multi-Tenancy
- Complete tenant isolation in database
- SuperAdmin can create new tenants via platform dashboard
- Each tenant has independent users, projects, and scans

### Role-Based Access Control
- Granular permissions system
- Route-level and component-level access control
- Each role sees only permitted actions and data

### Vulnerability Scanning
- Automated web application scanning
- Real-time risk scoring
- Severity classification (Critical, High, Medium, Low)
- Detailed vulnerability reports

### Compliance Reporting
- PDF export for scan results
- Audit-ready documentation
- SOC2, ISO 27001, GDPR, HIPAA tracking
- Audit log of all actions

### Modern UI/UX
- Glassmorphism design system
- Cyber security aesthetic
- Responsive layout
- Smooth animations
- Dark theme optimized

## ⚙️ Environment Variables

### Backend (.env)
```env
# App config
APP_NAME=CyberSec SaaS
ENVIRONMENT=development

# JWT
SECRET_KEY=<strong-secret-key>  # ⚠️ CHANGE IN PRODUCTION
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES_MINUTES=30
REFRESH_TOKEN_EXPIRES_DAYS=7

# Database
DATABASE_URL=postgresql+psycopg://user:pass@host:5432/dbname

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:5174

# Rate limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW_SECONDS=60

# Logging
LOG_LEVEL=INFO
```

### Frontend (.env - optional)
```env
VITE_API_URL=http://localhost:8000
```

## 🔌 API Endpoints

### Public API (No Authentication)

- `GET /public/status` - Live system status and aggregated metrics
- `GET /public/reports` - Published security reports (sanitized)

### Authentication

- `POST /auth/login` - Login and receive JWT tokens

### Internal API (JWT Authentication Required)

**Tenants (SuperAdmin only):**
- `POST /tenants` - Create new tenant
- `GET /tenants` - List all tenants

**Users:**
- `GET /users` - List users in current tenant

**Projects:**
- `POST /projects` - Create new project/target
- `GET /projects` - List projects in current tenant

**Scans:**
- `POST /scan/{project_id}` - Start new scan
- `GET /scan/{scan_id}` - Get scan details
- `GET /scans` - List scans in current tenant

**Reports:**
- `GET /report/{scan_id}` - Download full PDF report (internal)

Full API documentation available at http://localhost:8000/docs when server is running.

## 🚀 Deployment

### Backend (Render/Railway/Fly.io)

**Build command:**
```bash
pip install -r requirements.txt
```

**Start command:**
```bash
gunicorn -c uvicorn_config.py app.main:app
```

**Environment variables:**
- Set all variables from `.env.example`
- Use production PostgreSQL URL
- Generate strong `SECRET_KEY`: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- Set `ENVIRONMENT=production`

### Frontend (Vercel/Netlify)

**Framework:** Vite  
**Build command:**
```bash
npm run build
```

**Output directory:** `dist`  
**Environment variables:**
- `VITE_API_URL` - Your production backend URL

## 📊 Test Coverage

| Component | Test File | Tests | Status |
|-----------|-----------|-------|--------|
| Backend Risk Utils | tests/test_risk.py | 2 | ✅ Passing |
| Frontend Landing | src/__tests__/landing.test.jsx | 1 | ✅ Passing |

**Expand test coverage:**
- Backend: Add tests for auth, tenants, scans, reports
- Frontend: Add tests for dashboards, auth flow, API integration

## ⚠️ Known Issues

1. **Database Connection Error**
   - Neon PostgreSQL may auto-pause on free tier
   - Check https://console.neon.tech/ and resume database
   - Or switch to local PostgreSQL for development

2. **Port Conflicts**
   - Frontend may use port 5174 if 5173 is busy
   - Backend always uses 8000 unless specified

3. **Windows PATH**
   - pytest may not be on PATH - use full path: `C:\Users\<user>\AppData\Local\Python\pythoncore-3.14-64\Scripts\pytest.exe`

## 📝 Development Workflow

1. Start backend server: `uvicorn app.main:app --reload`
2. Start frontend dev server: `npm run dev`
3. Access landing page: http://localhost:5174/
4. Login with seeded SuperAdmin or create new user
5. Navigate to role-specific dashboard
6. Make code changes - both servers auto-reload

## 🤝 Contributing

1. Create feature branch from `main`
2. Make changes with tests
3. Run test suite (backend + frontend)
4. Submit pull request

## 📄 License

This project is for educational/demonstration purposes.

## 🔗 Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Router Documentation](https://reactrouter.com/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- [TailwindCSS Documentation](https://tailwindcss.com/)
