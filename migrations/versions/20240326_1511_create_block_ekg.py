"""create_block_ekg

Revision ID: bf13a3cfcbc5
Revises: 9fdc325aed89
Create Date: 2024-03-26 15:11:01.073681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf13a3cfcbc5'
down_revision: Union[str, None] = '9fdc325aed89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Команды для выполнения при миграции вверх
    op.execute("""
    CREATE TABLE public.appointment_block_ekgs (
        id SERIAL PRIMARY KEY,
        date_ekg TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        sinus_ritm BOOLEAN NOT NULL DEFAULT false,
        av_blokada BOOLEAN NOT NULL DEFAULT false,
        hypertrofia_lg BOOLEAN NOT NULL DEFAULT false,
        ritm_eks BOOLEAN NOT NULL DEFAULT false,
        av_uzlovaya_tahikardia BOOLEAN NOT NULL DEFAULT false,
        superventrikulyrnaya_tahikardia BOOLEAN NOT NULL DEFAULT false,
        zheludochnaya_tahikardia BOOLEAN NOT NULL DEFAULT false,
        fabrilycia_predcerdiy BOOLEAN NOT NULL DEFAULT false,
        trepetanie_predcerdiy BOOLEAN NOT NULL DEFAULT false,
        another_changes TEXT,
        date_echo_ekg TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        fv INTEGER NOT NULL,
        sdla INTEGER,
        lp INTEGER,
        pp INTEGER,
        kdr_lg INTEGER,
        ksr_lg INTEGER,
        kdo_lg INTEGER,
        mgp INTEGER,
        zslg INTEGER,
        local_hypokines BOOLEAN NOT NULL DEFAULT false,
        distol_disfunction BOOLEAN NOT NULL DEFAULT false,
        anevrizma BOOLEAN NOT NULL DEFAULT false,
        note TEXT
    );
    """)

def downgrade():
    # Команды для выполнения при откате миграции
    op.execute("""
    DROP TABLE public.appointment_block_ekgs;
    """)