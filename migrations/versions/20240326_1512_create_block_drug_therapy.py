"""create_block_drug_therapy

Revision ID: 8a1dbf4423b2
Revises: 6525415a6f99
Create Date: 2024-03-26 15:11:52.139637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a1dbf4423b2'
down_revision: Union[str, None] = '6525415a6f99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
