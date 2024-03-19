"""create general urine analyse

Revision ID: 1b1cc569bbc6
Revises: a9105b9d518f
Create Date: 2024-03-19 12:02:34.020931

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b1cc569bbc6'
down_revision: Union[str, None] = 'a9105b9d518f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.general_urine_analyses (
    id serial constraint general_urine_analyse_pk
        primary key,
    protein float,
    protein_date timestamp without time zone,
    red_blood_cells float,
    red_blood_cells_date timestamp without time zone,
    leukocytes float,
    leukocytes_date timestamp without time zone,
    note text
    );
    ''')


def downgrade() -> None:
    op.execute('drop table public.general_urine_analyses;')

