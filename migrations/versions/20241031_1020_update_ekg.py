"""update ekg

Revision ID: d1a12ba5555c
Revises: b80b256ac835
Create Date: 2024-10-31 10:20:45.158383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1a12ba5555c'
down_revision: Union[str, None] = 'b80b256ac835'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    ALTER TABLE appointment_block_ekgs ADD COLUMN lp2 float;
    ''')
    op.execute('''
    ALTER TABLE appointment_block_ekgs ADD COLUMN pp2 float;
    ''')
    op.execute('''
    ALTER TABLE appointment_block_ekgs ADD COLUMN kso_lg float;
    ''')



def downgrade() -> None:
    op.execute('''
    ALTER TABLE appointment_block_ekgs DROP COLUMN kso_lg CASCADE;
    ''')
    op.execute('''
    ALTER TABLE appointment_block_ekgs DROP COLUMN pp2 CASCADE;
    ''')
    op.execute('''
    ALTER TABLE appointment_block_ekgs DROP COLUMN lp2 CASCADE;
    ''')
