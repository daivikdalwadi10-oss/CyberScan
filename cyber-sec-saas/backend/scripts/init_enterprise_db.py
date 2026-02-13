"""
Initialize enterprise database schema
Creates all tables from enterprise models
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import Base, engine
from app.models import enterprise_models

async def init_enterprise_db():
    """Create all enterprise database tables"""
    print("🗄️  Initializing enterprise database schema...\n")

    # Import all models to ensure they're registered
    print("📦 Loading models:")
    print("   - Users & Roles")
    print("   - Audit Logs")
    print("   - Alerts & Incidents")
    print("   - Threat Intelligence")
    print("   - Cloud Status")
    print("   - Uptime Records")
    print("   - System Metrics")
    print("   - Risk Scores\n")

    print("🔨 Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("\n✅ Database initialized successfully!\n")
    print("Created tables:")
    for table in Base.metadata.sorted_tables:
        print(f"  ✓ {table.name}")

    print("\n" + "=" * 60)
    print("Next steps:")
    print("  1. Run: python scripts/init_enterprise_roles.py")
    print("  2. Run: python scripts/seed_enterprise_users.py")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(init_enterprise_db())
