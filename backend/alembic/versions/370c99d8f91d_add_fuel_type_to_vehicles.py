"""add fuel_type to vehicles

Revision ID: 370c99d8f91d
Revises: 1702e3334605
Create Date: 2026-08-03 12:13:05.192463

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '370c99d8f91d'
down_revision: Union[str, Sequence[str], None] = '1702e3334605'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:

    # 1. Add column temporarily nullable
    op.add_column(
        'vehicles',
        sa.Column(
            'fuel_type',
            sa.String(length=30),
            nullable=True
        )
    )


    # 2. Give existing vehicles default fuel type
    op.execute(
        """
        UPDATE vehicles
        SET fuel_type = 'DIESEL'
        WHERE fuel_type IS NULL
        """
    )


    # 3. Make column mandatory
    op.alter_column(
        'vehicles',
        'fuel_type',
        existing_type=sa.String(length=30),
        nullable=False
    )



def downgrade() -> None:

    op.drop_column(
        'vehicles',
        'fuel_type'
    )