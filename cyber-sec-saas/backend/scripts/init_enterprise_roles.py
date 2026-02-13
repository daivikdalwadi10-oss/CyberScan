"""
Initialize predefined enterprise roles with permissions
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models.enterprise_models import Role, RoleType

# Define role permissions
ROLE_PERMISSIONS = {
    RoleType.SUPER_ADMIN: {
        "display_name": "Super Administrator",
        "description": "Full platform access - user management, system configuration, all data",
        "permissions": [
            "user:create", "user:read", "user:update", "user:delete",
            "role:assign", "role:revoke",
            "alert:read", "alert:acknowledge", "alert:resolve", "alert:delete",
            "incident:create", "incident:read", "incident:update", "incident:delete", "incident:assign",
            "audit:read", "audit:export",
            "threat:read", "cloud:read", "metrics:read",
            "risk:read",
            "system:configure", "system:restart",
            "dashboard:all"
        ]
    },
    RoleType.SECURITY_ADMIN: {
        "display_name": "Security Administrator",
        "description": "Manage security operations, alerts, incidents, and SOC team",
        "permissions": [
            "user:read",
            "alert:read", "alert:acknowledge", "alert:resolve",
            "incident:create", "incident:read", "incident:update", "incident:assign",
            "audit:read",
            "threat:read", "cloud:read", "metrics:read",
            "risk:read",
            "dashboard:security_admin"
        ]
    },
    RoleType.SOC_ANALYST: {
        "display_name": "SOC Analyst",
        "description": "Monitor alerts, investigate threats, manage incidents",
        "permissions": [
            "alert:read", "alert:acknowledge",
            "incident:create", "incident:read", "incident:update",
            "threat:read", "cloud:read",
            "risk:read",
            "dashboard:soc_analyst"
        ]
    },
    RoleType.INFRA_ADMIN: {
        "display_name": "Infrastructure Administrator",
        "description": "Monitor infrastructure health, system metrics, uptime",
        "permissions": [
            "alert:read",
            "cloud:read", "metrics:read",
            "uptime:read",
            "dashboard:infra_admin"
        ]
    },
    RoleType.COMPLIANCE_OFFICER: {
        "display_name": "Compliance Officer",
        "description": "Audit logs, risk scores, compliance reporting",
        "permissions": [
            "audit:read", "audit:export",
            "risk:read",
            "incident:read",
            "dashboard:compliance_officer"
        ]
    },
    RoleType.AUDITOR: {
        "display_name": "Auditor",
        "description": "Read-only access to logs, reports, and historical data",
        "permissions": [
            "audit:read",
            "risk:read",
            "incident:read",
            "alert:read",
            "dashboard:auditor"
        ]
    },
    RoleType.INTERNAL_USER: {
        "display_name": "Internal User",
        "description": "Limited read-only access to basic metrics",
        "permissions": [
            "risk:read",
            "dashboard:internal_user"
        ]
    },
    RoleType.PUBLIC_VISITOR: {
        "display_name": "Public Visitor",
        "description": "Public transparency dashboard only",
        "permissions": [
            "dashboard:public"
        ]
    }
}


async def init_roles():
    """Create predefined roles in database"""
    async with AsyncSessionLocal() as db:
        try:
            print("🔐 Initializing enterprise roles...\n")

            result = await db.execute(select(Role))
            existing_roles = {role.role_type: role for role in result.scalars().all()}

            for role_type, config in ROLE_PERMISSIONS.items():
                existing = existing_roles.get(role_type)

                if existing:
                    # Update existing role
                    existing.display_name = config["display_name"]
                    existing.description = config["description"]
                    existing.permissions = config["permissions"]
                    print(
                        f"✅ Updated: {config['display_name']} ({len(config['permissions'])} permissions)"
                    )
                else:
                    # Create new role
                    role = Role(
                        role_type=role_type,
                        display_name=config["display_name"],
                        description=config["description"],
                        permissions=config["permissions"],
                    )
                    db.add(role)
                    print(
                        f"✅ Created: {config['display_name']} ({len(config['permissions'])} permissions)"
                    )

            await db.commit()

            print("\n" + "=" * 60)
            print("🎉 Role initialization complete!")
            print("=" * 60)
            print(f"\nTotal roles: {len(ROLE_PERMISSIONS)}")
            print("\nRole Hierarchy:")
            print("  1. SuperAdmin          - Full platform control")
            print("  2. SecurityAdmin       - Security operations")
            print("  3. SOCAnalyst         - Threat monitoring")
            print("  4. InfraAdmin         - Infrastructure monitoring")
            print("  5. ComplianceOfficer  - Audit & compliance")
            print("  6. Auditor            - Read-only auditing")
            print("  7. InternalUser       - Limited internal access")
            print("  8. PublicVisitor      - Public dashboard only")
            print()
        except Exception as exc:
            await db.rollback()
            print(f"\n❌ Error initializing roles: {exc}")
            raise


if __name__ == "__main__":
    asyncio.run(init_roles())
