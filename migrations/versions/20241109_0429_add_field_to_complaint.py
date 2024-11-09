"""add field to complaint

Revision ID: 808278db5329
Revises: d1a12ba5555c
Create Date: 2024-11-09 04:29:16.462864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '808278db5329'
down_revision: Union[str, None] = 'd1a12ba5555c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    ALTER TABLE public.appointment_block_complaints ADD COLUMN IF NOT EXISTS
        heart_problems boolean not null default false;
    ''')


def downgrade() -> None:
    op.execute('''
    ALTER TABLE public.appointment_block_complaints DROP COLUMN IF EXISTS
        heart_problems;
    ''')
