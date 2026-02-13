"""
Seed script to create test users for all 7 roles.
Run this after database connection is restored.
"""
from app.database import SessionLocal
from app.models.models_legacy_ARCHIVED import (
    LegacyUser as User,
    LegacyTenant as Tenant,
    LegacyRole as Role
)
from app.auth.password import hash_password
from datetime import datetime

# Test user credentials
TEST_USERS = [
    # SuperAdmin - Platform-level access
    {
        "email": "superadmin@platform.local",
        "password": "Super@123",
        "role": Role.super_admin,
        "tenant_name": "Platform"
    },
    # TenantAdmin - Organization admin
    {
        "email": "admin@acme.com",
        "password": "Admin@123",
        "role": Role.admin,
        "tenant_name": "Acme Corporation"
    },
    # SecurityManager - Approval workflows
    {
        "email": "manager@acme.com",
        "password": "Manager@123",
        "role": Role.admin,  # Backend uses 'admin' for tenant admins
        "tenant_name": "Acme Corporation"
    },
    # SecurityAnalyst - Vulnerability analysis
    {
        "email": "analyst@acme.com",
        "password": "Analyst@123",
        "role": Role.analyst,
        "tenant_name": "Acme Corporation"
    },
    # SOCOperator - Real-time monitoring
    {
        "email": "soc@acme.com",
        "password": "Soc@123",
        "role": Role.analyst,  # Backend uses 'analyst' role
        "tenant_name": "Acme Corporation"
    },
    # Auditor - Compliance reporting
    {
        "email": "auditor@acme.com",
        "password": "Auditor@123",
        "role": Role.viewer,  # Backend uses 'viewer' for read-only
        "tenant_name": "Acme Corporation"
    },
    # Viewer - Read-only access
    {
        "email": "viewer@acme.com",
        "password": "Viewer@123",
        "role": Role.viewer,
        "tenant_name": "Acme Corporation"
    },
    # Additional tenant for testing
    {
        "email": "admin@techcorp.com",
        "password": "Admin@123",
        "role": Role.admin,
        "tenant_name": "TechCorp"
    }
]

def seed_test_users():
    db = SessionLocal()
    try:
        print("🌱 Seeding test users...\n")
        
        # Track created tenants to avoid duplicates
        tenant_cache = {}
        
        for user_data in TEST_USERS:
            tenant_name = user_data["tenant_name"]
            
            # Create or get tenant
            if tenant_name not in tenant_cache:
                tenant = db.query(Tenant).filter(Tenant.name == tenant_name).first()
                if not tenant:
                    tenant = Tenant(name=tenant_name, created_at=datetime.utcnow())
                    db.add(tenant)
                    db.flush()
                    print(f"✅ Created tenant: {tenant_name}")
                else:
                    print(f"ℹ️  Using existing tenant: {tenant_name}")
                tenant_cache[tenant_name] = tenant
            else:
                tenant = tenant_cache[tenant_name]
            
            # Check if user exists
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if existing_user:
                print(f"⚠️  User already exists: {user_data['email']}")
                continue
            
            # Create user
            user = User(
                email=user_data["email"],
                hashed_password=hash_password(user_data["password"]),
                role=user_data["role"],
                tenant_id=tenant.id,
                created_at=datetime.utcnow()
            )
            db.add(user)
            print(f"✅ Created user: {user_data['email']} ({user_data['role'].value})")
        
        db.commit()
        print(f"\n🎉 Successfully seeded {len(TEST_USERS)} test users!")
        print("\n" + "="*60)
        print("TEST CREDENTIALS")
        print("="*60)
        print("\n🔐 SuperAdmin (Platform Level)")
        print("   Email: superadmin@platform.local")
        print("   Password: Super@123")
        print("   Dashboard: /portal/dashboard/super-admin")
        
        print("\n🏢 TenantAdmin (Acme Corporation)")
        print("   Email: admin@acme.com")
        print("   Password: Admin@123")
        print("   Dashboard: /portal/dashboard/tenant-admin")
        
        print("\n👔 SecurityManager (Acme Corporation)")
        print("   Email: manager@acme.com")
        print("   Password: Manager@123")
        print("   Dashboard: /portal/dashboard/manager")
        
        print("\n🔍 SecurityAnalyst (Acme Corporation)")
        print("   Email: analyst@acme.com")
        print("   Password: Analyst@123")
        print("   Dashboard: /portal/dashboard/analyst")
        
        print("\n🚨 SOCOperator (Acme Corporation)")
        print("   Email: soc@acme.com")
        print("   Password: Soc@123")
        print("   Dashboard: /portal/dashboard/soc")
        
        print("\n📋 Auditor (Acme Corporation)")
        print("   Email: auditor@acme.com")
        print("   Password: Auditor@123")
        print("   Dashboard: /portal/dashboard/auditor")
        
        print("\n👁️  Viewer (Acme Corporation)")
        print("   Email: viewer@acme.com")
        print("   Password: Viewer@123")
        print("   Dashboard: /portal/dashboard/viewer")
        
        print("\n🏢 TenantAdmin (TechCorp)")
        print("   Email: admin@techcorp.com")
        print("   Password: Admin@123")
        print("   Dashboard: /portal/dashboard/tenant-admin")
        
        print("\n" + "="*60)
        print("Login at: http://localhost:5175/portal/login")
        print("="*60 + "\n")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error seeding users: {e}")
        print("\n⚠️  Make sure database connection is working!")
        print("   Check STATUS.md for database troubleshooting steps.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_test_users()
