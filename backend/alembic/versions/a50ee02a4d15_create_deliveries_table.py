"""create deliveries table

Revision ID: a50ee02a4d15
Revises: 7aadccb1d24d

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "a50ee02a4d15"
down_revision: Union[str, Sequence[str], None] = "7aadccb1d24d"
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


def upgrade():

    bind = op.get_bind()

    # create enum only if missing
    delivery_status_enum.create(
        bind,
        checkfirst=True
    )


    op.create_table(
        "deliveries",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "tracking_number",
            sa.String(length=50),
            nullable=False
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
            nullable=False
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
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),

        sa.UniqueConstraint(
            "tracking_number"
        )
    )


    op.create_index(
        "ix_deliveries_id",
        "deliveries",
        ["id"],
        unique=False
    )



def downgrade():

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