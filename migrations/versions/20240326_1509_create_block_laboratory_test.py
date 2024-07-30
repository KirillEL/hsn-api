"""create_block_laboratory_test

Revision ID: 9fdc325aed89
Revises: 2318f2994dcf
Create Date: 2024-03-26 15:09:45.741819

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9fdc325aed89"
down_revision: Union[str, None] = "2318f2994dcf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
    create table public.appointment_block_laboratory_tests (
    id serial constraint appointment_block_laboratory_test_pk primary key,
    nt_pro_bnp float,
    nt_pro_bnp_date varchar(10),
    hbalc float,
    hbalc_date varchar(10),
    
    eritrocit float,
    eritrocit_date varchar(10),
    hemoglobin float,
    hemoglobin_date varchar(10),
    
    tg float,
    tg_date varchar(10),
    lpvp float,
    lpvp_date varchar(10),
    lpnp float,
    lpnp_date varchar(10),
    general_hc float,
    general_hc_date varchar(10),
    natriy float,
    natriy_date varchar(10),
    kaliy float,
    kaliy_date varchar(10),
    glukoza float,
    glukoza_date varchar(10),
    mochevaya_kislota float, 
    mochevaya_kislota_date varchar(10),
    skf float,
    skf_date varchar(10),
    kreatinin float,
    kreatinin_date varchar(10),
    protein float,
    protein_date varchar(10),
    urine_eritrocit float,
    urine_eritrocit_date varchar(10),
    urine_leycocit float,
    urine_leycocit_date varchar(10),
    microalbumuria float,
    microalbumuria_date varchar(10),
    note text
    );
    """
    )


def downgrade() -> None:
    op.execute("drop table public.appointment_block_laboratory_tests;")
