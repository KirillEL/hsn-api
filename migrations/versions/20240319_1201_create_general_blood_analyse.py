"""create general blood analyse

Revision ID: 07611266950e
Revises: 4741c3fede2c
Create Date: 2024-03-19 12:01:54.673800

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07611266950e'
down_revision: Union[str, None] = '4741c3fede2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.general_blood_analyses (
    id serial constraint general_blood_analyse_pk
        primary key,
    gemoglobin float,
    gemoglobin_date timestamp without time zone
    );
    ''')


def downgrade() -> None:
    op.execute('drop table public.general_blood_analyses;')

