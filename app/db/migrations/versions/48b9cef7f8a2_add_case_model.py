"""Add case model

Revision ID: 48b9cef7f8a2
Revises: 2a0a7fdef0f6
Create Date: 2024-09-06 13:37:27.178152

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "48b9cef7f8a2"
down_revision = "2a0a7fdef0f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cases",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "category",
            sa.Enum(
                "asylum",
                "crime",
                "debt",
                "family",
                "housing",
                "welfare",
                name="category",
            ),
            nullable=True,
        ),
        sa.Column("exceptional_funding", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("cases")
