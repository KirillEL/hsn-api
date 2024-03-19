"""create blood chemistry

Revision ID: 4741c3fede2c
Revises: 5230121539e4
Create Date: 2024-03-19 11:46:12.007372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4741c3fede2c'
down_revision: Union[str, None] = '5230121539e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.blood_chemistries (
    id serial constraint blood_chemistry_pk primary key,
    lpnp float,
    lpnp_date timestamp without time zone,
    general_hs float,
    general_hs_date timestamp without time zone,
    natriy float,
    natriy_date timestamp without time zone,
    kaliy float,
    kaliy_date timestamp without time zone,
    ferritin float,
    ferritin_date timestamp without time zone,
    transferrin float,
    transferrin_date timestamp without time zone,
    glukoza float,
    glukoza_date timestamp without time zone,
    mochevaya_kta float,
    mochevaya_kta_date timestamp without time zone,
    skf float,
    skf_date timestamp without time zone,
    kreatin float,
    kreatin_date timestamp without time zone
    );
    ''')


def downgrade() -> None:
    op.execute('drop table public.blood_chemistries;')
