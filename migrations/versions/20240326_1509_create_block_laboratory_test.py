"""create_block_laboratory_test

Revision ID: 9fdc325aed89
Revises: 2318f2994dcf
Create Date: 2024-03-26 15:09:45.741819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fdc325aed89'
down_revision: Union[str, None] = '2318f2994dcf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.appointment_block_laboratory_tests (
    id serial constraint appointment_block_laboratory_test_pk primary key,
    nt_pro_bnp float,
    nt_pro_bnp_date timestamp without time zone,
    hbalc float,
    hbalc_date timestamp without time zone,
    
    eritrocit float,
    eritrocit_date timestamp without time zone,
    hemoglobin float,
    hemoglobin_date timestamp without time zone,
    
    tg float,
    tg_date timestamp without time zone,
    lpvp float,
    lpvp_date timestamp without time zone,
    lpnp float,
    lpnp_date timestamp without time zone,
    general_hc float,
    general_hc_date timestamp without time zone,
    natriy float,
    natriy_date timestamp without time zone,
    kaliy float,
    kaliy_date timestamp without time zone,
    glukoza float,
    glukoza_date timestamp without time zone,
    mochevaya_kislota float, 
    mochevaya_kislota_date timestamp without time zone,
    skf float,
    skf_date timestamp without time zone,
    kreatinin float,
    kreatinin_date timestamp without time zone,
    protein float,
    protein_date timestamp without time zone,
    urine_eritrocit float,
    urine_eritrocit_date timestamp without time zone,
    urine_leycocit float,
    urine_leycocit_date timestamp without time zone,
    microalbumuria float,
    microalbumuria_date timestamp without time zone,
    note text
    );
    ''')


def downgrade() -> None:
    op.execute('drop table public.appointment_block_laboratory_tests;')

