"""change type fields in lab-tests

Revision ID: 05f580b88a46
Revises: 808278db5329
Create Date: 2024-11-10 05:38:33.351397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05f580b88a46'
down_revision: Union[str, None] = '808278db5329'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    ALTER TABLE public.appointment_block_laboratory_tests
        ALTER COLUMN protein TYPE varchar(50),
        ALTER COLUMN urine_eritrocit TYPE varchar(50),
        ALTER COLUMN urine_leycocit TYPE varchar(50),
        ALTER COLUMN microalbumuria TYPE varchar(50);
    ''')


def downgrade() -> None:
    op.execute('''    
    ALTER TABLE public.appointment_block_laboratory_tests
        ALTER COLUMN protein TYPE float,
        ALTER COLUMN urine_eritrocit TYPE float,
        ALTER COLUMN urine_leycocit TYPE float,
        ALTER COLUMN microalbumuria TYPE float;
    ''')
