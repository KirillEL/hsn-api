"""change ekg date

Revision ID: 2639d6fa7326
Revises: 05f580b88a46
Create Date: 2024-11-13 04:43:28.024940

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2639d6fa7326'
down_revision: Union[str, None] = '05f580b88a46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    ALTER TABLE public.appointment_block_ekgs
    ALTER COLUMN date_ekg DROP NOT NULL;
    ''')


def downgrade() -> None:
    op.execute('''
    ALTER TABLE public.appointment_block_ekgs
    ALTER COLUMN date_ekg SET NOT NULL;
    ''')
