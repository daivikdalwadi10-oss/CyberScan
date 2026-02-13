import os
import sys

from app.auth.password import hash_password
from app.database import Base, SessionLocal, engine
from app.models import Role, Tenant, User


def main() -> int:
    email = os.getenv("SUPER_ADMIN_EMAIL")
    password = os.getenv("SUPER_ADMIN_PASSWORD")
    tenant_name = os.getenv("SUPER_ADMIN_TENANT", "Platform")

    if not email or not password:
        print("Missing SUPER_ADMIN_EMAIL or SUPER_ADMIN_PASSWORD")
        return 1

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        tenant = db.query(Tenant).filter(Tenant.name == tenant_name).first()
        if not tenant:
            tenant = Tenant(name=tenant_name)
            db.add(tenant)
            db.commit()
            db.refresh(tenant)

        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print("Super admin already exists")
            return 0

        user = User(
            email=email,
            hashed_password=hash_password(password),
            role=Role.super_admin,
            tenant_id=tenant.id,
        )
        db.add(user)
        db.commit()
        print(f"Created SuperAdmin {email} in tenant {tenant.id}")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
