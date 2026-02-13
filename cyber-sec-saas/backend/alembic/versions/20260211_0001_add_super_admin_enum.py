from alembic import op

revision = "20260211_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return

    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'role') THEN
                IF NOT EXISTS (
                    SELECT 1
                    FROM pg_enum e
                    JOIN pg_type t ON e.enumtypid = t.oid
                    WHERE t.typname = 'role' AND e.enumlabel = 'SuperAdmin'
                ) THEN
                    ALTER TYPE role ADD VALUE 'SuperAdmin';
                END IF;
            END IF;
        END $$;
        """
    )


def downgrade() -> None:
    pass
