"""create hormonal blood analyse

Revision ID: a9105b9d518f
Revises: 07611266950e
Create Date: 2024-03-19 12:02:10.847039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9105b9d518f'
down_revision: Union[str, None] = '07611266950e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table hormonal_blood_analyses (
    id serial constraint hormonal_blood_analyse_pk
        primary key,
    nt_pro_bnp float,
    nt_pro_bnp_date timestamp without time zone,
    hba1c float,
    hba1c_date timestamp without time zone
    );
    ''')


def downgrade() -> None:
    op.execute('drop table hormonal_blood_analyses;')

