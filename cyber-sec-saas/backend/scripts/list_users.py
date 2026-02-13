"""List all users in the database"""
from app.database import SessionLocal
from app.models.models import User

db = SessionLocal()
try:
    users = db.query(User).all()
    if not users:
        print("No users found in database.")
    else:
        print(f"\nFound {len(users)} users:")
        print("-" * 60)
        for user in users:
            print(f"Email: {user.email}")
            print(f"Role: {user.role.value}")
            print(f"Tenant ID: {user.tenant_id}")
            print("-" * 60)
except Exception as e:
    print(f"Error: {e}")
    print("\nDatabase connection failed. No users available.")
finally:
    db.close()
