"""update patient clinic

Revision ID: 626074bfd6fd
Revises: 2639d6fa7326
Create Date: 2024-11-24 04:51:52.744846

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '626074bfd6fd'
down_revision: Union[str, None] = '2639d6fa7326'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('ALTER TABLE public.patients ALTER COLUMN clinic DROP NOT NULL;')


def downgrade() -> None:
    op.execute('ALTER TABLE public.patients ALTER COLUMN clinic SET NOT NULL;')
