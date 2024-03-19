"""creaate appointment laboratory test

Revision ID: 5230121539e4
Revises: 94d7a99f5b44
Create Date: 2024-03-19 11:45:50.633609

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5230121539e4'
down_revision: Union[str, None] = '94d7a99f5b44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.appointment_laboratory_tests (
    id serial constraint appointment_laboratory_test_pk
        primary key,
    nt_pro_bnp float,
    nt_pro_bnp_date timestamp without time zone,
    microalbumuria float,
    microalbumuria_date timestamp without time zone
    );
    ''')


def downgrade() -> None:
    op.execute('drop table public.appointment_laboratory_tests;')
