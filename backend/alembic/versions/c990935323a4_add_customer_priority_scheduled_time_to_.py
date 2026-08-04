"""add customer priority scheduled time to deliveries

Revision ID: c990935323a4
Revises: b2d06571ead1
Create Date: 2026-08-01 13:08:14.283398
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c990935323a4"
down_revision: Union[str, Sequence[str], None] = "b2d06571ead1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # Create enum type
    priority_enum = sa.Enum(
        "LOW",
        "MEDIUM",
        "HIGH",
        name="deliverypriority",
    )
    priority_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "deliveries",
        sa.Column(
            "customer_name",
            sa.String(100),
            nullable=True,
            server_default="Unknown Customer",
        ),
    )

    op.add_column(
        "deliveries",
        sa.Column(
            "priority",
            sa.Enum(
                "LOW",
                "MEDIUM",
                "HIGH",
                name="deliverypriority",
                create_type=False,
            ),
            nullable=True,
            server_default="MEDIUM",
        ),
    )

    op.add_column(
        "deliveries",
        sa.Column(
            "scheduled_time",
            sa.DateTime(),
            nullable=True,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )

    # Remove defaults
    op.alter_column(
        "deliveries",
        "customer_name",
        server_default=None,
    )

    op.alter_column(
        "deliveries",
        "priority",
        server_default=None,
    )

    op.alter_column(
        "deliveries",
        "scheduled_time",
        server_default=None,
    )


def downgrade() -> None:

    op.drop_column("deliveries", "scheduled_time")
    op.drop_column("deliveries", "priority")
    op.drop_column("deliveries", "customer_name")

    sa.Enum(
        "LOW",
        "MEDIUM",
        "HIGH",
        name="deliverypriority",
    ).drop(op.get_bind(), checkfirst=True)