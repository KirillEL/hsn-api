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
    nt_pro_bnp_date varchar(12),
    hbalc float,
    hbalc_date varchar(12),
    
    eritrocit float,
    hemoglobin float,
    oak_date varchar(12),
    
    tg float,
    lpvp float,
    lpnp float,
    general_hc float,
    natriy float,
    kaliy float,
    glukoza float,
    mochevaya_kislota float, 
    skf float,
    kreatinin float,
    bk_date varchar(12),
    
    protein float,
    urine_eritrocit float,
    urine_leycocit float,
    microalbumuria float,
    am_date varchar(12),
    note text
    );
    """
    )


def downgrade() -> None:
    op.execute("drop table public.appointment_block_laboratory_tests;")
