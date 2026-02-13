"""
Seed enterprise test users with new role system
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import AsyncSessionLocal
from app.models.enterprise_models import User, Role, RoleType, user_roles
from app.auth.password import hash_password
from datetime import datetime
import uuid

# Test users for each role
TEST_USERS = [
    {
        "email": "superadmin@cybersecurity.io",
        "password": "Super@2026!",
        "full_name": "Platform Super Administrator",
        "roles": [RoleType.SUPER_ADMIN]
    },
    {
        "email": "sec.admin@cybersecurity.io",
        "password": "SecAdmin@2026!",
        "full_name": "Security Administrator",
        "roles": [RoleType.SECURITY_ADMIN]
    },
    {
        "email": "soc.analyst@cybersecurity.io",
        "password": "SOC@2026!",
        "full_name": "SOC Analyst - Alice Johnson",
        "roles": [RoleType.SOC_ANALYST]
    },
    {
        "email": "soc2.analyst@cybersecurity.io",
        "password": "SOC@2026!",
        "full_name": "SOC Analyst - Bob Martinez",
        "roles": [RoleType.SOC_ANALYST]
    },
    {
        "email": "infra.admin@cybersecurity.io",
        "password": "Infra@2026!",
        "full_name": "Infrastructure Administrator",
        "roles": [RoleType.INFRA_ADMIN]
    },
    {
        "email": "compliance@cybersecurity.io",
        "password": "Compliance@2026!",
        "full_name": "Compliance Officer",
        "roles": [RoleType.COMPLIANCE_OFFICER]
    },
    {
        "email": "auditor@cybersecurity.io",
        "password": "Audit@2026!",
        "full_name": "External Auditor",
        "roles": [RoleType.AUDITOR]
    },
    {
        "email": "internal.user@cybersecurity.io",
        "password": "User@2026!",
        "full_name": "Internal Employee",
        "roles": [RoleType.INTERNAL_USER]
    },
    # Multi-role user for testing
    {
        "email": "hybrid.admin@cybersecurity.io",
        "password": "Hybrid@2026!",
        "full_name": "Hybrid Admin (Security + Infra)",
        "roles": [RoleType.SECURITY_ADMIN, RoleType.INFRA_ADMIN]
    }
]


async def seed_enterprise_users():
    """Create enterprise test users with role assignments"""
    async with AsyncSessionLocal() as db:
        try:
            print("👥 Seeding enterprise users...\n")

            # Get all roles from database
            roles_result = await db.execute(select(Role))
            roles_db = {r.role_type: r for r in roles_result.scalars().all()}

            if not roles_db:
                print("❌ No roles found! Run init_enterprise_roles.py first.")
                return

            created_count = 0
            updated_count = 0

            for user_data in TEST_USERS:
                user_result = await db.execute(
                    select(User)
                    .options(selectinload(User.roles))
                    .where(User.email == user_data["email"])
                )
                existing = user_result.scalar_one_or_none()

                if existing:
                    # Update existing user
                    existing.full_name = user_data["full_name"]
                    existing.is_active = True  # type: ignore[assignment]
                    # Clear existing roles
                    existing.roles.clear()
                    user = existing
                    updated_count += 1
                    action = "Updated"
                else:
                    # Create new user
                    user = User(
                        id=uuid.uuid4(),
                        email=user_data["email"],
                        hashed_password=hash_password(user_data["password"]),
                        full_name=user_data["full_name"],
                        is_active=True,
                        is_locked=False,
                        failed_login_attempts=0,
                    )
                    db.add(user)
                    created_count += 1
                    action = "Created"

                # Assign roles
                for role_type in user_data["roles"]:
                    if role_type in roles_db:
                        if role_type not in [r.role_type for r in user.roles]:
                            user.roles.append(roles_db[role_type])

                role_names = ", ".join([r.value for r in user_data["roles"]])
                print(f"✅ {action}: {user_data['full_name']}")
                print(f"   Email: {user_data['email']}")
                print(f"   Roles: {role_names}")
                print()

            await db.commit()

            print("=" * 70)
            print("🎉 User seeding complete!")
            print("=" * 70)
            print(f"\nCreated: {created_count}")
            print(f"Updated: {updated_count}")
            print(f"Total Users: {len(TEST_USERS)}")

            print("\n" + "=" * 70)
            print("LOGIN CREDENTIALS")
            print("=" * 70 + "\n")
            print("🔴 SUPER ADMIN")
            print("   Email: superadmin@cybersecurity.io")
            print("   Password: Super@2026!")
            print("   Access: Full platform control\n")

            print("🟠 SECURITY ADMIN")
            print("   Email: sec.admin@cybersecurity.io")
            print("   Password: SecAdmin@2026!")
            print("   Access: Security operations, alerts, incidents\n")

            print("🟡 SOC ANALYST")
            print("   Email: soc.analyst@cybersecurity.io")
            print("   Password: SOC@2026!")
            print("   Access: Threat monitoring, incident response\n")

            print("🔵 INFRASTRUCTURE ADMIN")
            print("   Email: infra.admin@cybersecurity.io")
            print("   Password: Infra@2026!")
            print("   Access: Infrastructure metrics, uptime\n")

            print("🟣 COMPLIANCE OFFICER")
            print("   Email: compliance@cybersecurity.io")
            print("   Password: Compliance@2026!")
            print("   Access: Audit logs, risk scores\n")

            print("⚪ AUDITOR")
            print("   Email: auditor@cybersecurity.io")
            print("   Password: Audit@2026!")
            print("   Access: Read-only audit access\n")

            print("⚫ INTERNAL USER")
            print("   Email: internal.user@cybersecurity.io")
            print("   Password: User@2026!")
            print("   Access: Limited internal metrics\n")

            print("=" * 70)
            print("Login at: http://localhost:5175/portal/login")
            print("Public Dashboard: http://localhost:5175/")
            print("=" * 70 + "\n")
        
        except Exception as exc:
            await db.rollback()
            print(f"\n❌ Error seeding users: {exc}")
            raise


if __name__ == "__main__":
    asyncio.run(seed_enterprise_users())
