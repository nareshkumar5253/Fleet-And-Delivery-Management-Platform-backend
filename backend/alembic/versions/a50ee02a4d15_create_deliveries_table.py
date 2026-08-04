"""create deliveries table

Revision ID: a50ee02a4d15
Revises: 2a7a32dfad69

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "a50ee02a4d15"

# IMPORTANT:
# deliveries depends on drivers table
down_revision: Union[str, Sequence[str], None] = "2a7a32dfad69"

branch_labels = None
depends_on = None


delivery_status_enum = postgresql.ENUM(
    "PENDING",
    "ASSIGNED",
    "IN_TRANSIT",
    "DELIVERED",
    "CANCELLED",
    name="deliverystatus"
)


def upgrade() -> None:

    bind = op.get_bind()

    # Create enum type
    delivery_status_enum.create(
        bind,
        checkfirst=True
    )


    op.create_table(
        "deliveries",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            "tracking_number",
            sa.String(length=50),
            nullable=False,
            unique=True
        ),

        sa.Column(
            "pickup_address",
            sa.String(length=255),
            nullable=False
        ),

        sa.Column(
            "delivery_address",
            sa.String(length=255),
            nullable=False
        ),

        sa.Column(
            "package_weight",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "status",
            postgresql.ENUM(
                "PENDING",
                "ASSIGNED",
                "IN_TRANSIT",
                "DELIVERED",
                "CANCELLED",
                name="deliverystatus",
                create_type=False
            ),
            nullable=False,
            server_default="PENDING"
        ),

        sa.Column(
            "driver_id",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False
        ),


        sa.ForeignKeyConstraint(
            ["driver_id"],
            ["drivers.id"]
        )
    )


    op.create_index(
        "ix_deliveries_id",
        "deliveries",
        ["id"],
        unique=False
    )



def downgrade() -> None:

    op.drop_index(
        "ix_deliveries_id",
        table_name="deliveries"
    )

    op.drop_table(
        "deliveries"
    )


    delivery_status_enum.drop(
        op.get_bind(),
        checkfirst=True
    )