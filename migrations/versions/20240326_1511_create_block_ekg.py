"""create_block_ekg

Revision ID: bf13a3cfcbc5
Revises: 9fdc325aed89
Create Date: 2024-03-26 15:11:01.073681

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bf13a3cfcbc5"
down_revision: Union[str, None] = "72e38a033c20"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        """
    CREATE TABLE public.appointment_block_ekgs (
        id SERIAL PRIMARY KEY,
        date_ekg TEXT NOT NULL,
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
        date_echo_ekg TEXT NOT NULL,
        fv float NOT NULL,
        sdla FLOAT,
        lp FLOAT,
        pp FLOAT,
        kdr_lg FLOAT,
        ksr_lg FLOAT,
        kdo_lg FLOAT,
        mgp FLOAT,
        zslg FLOAT,
        local_hypokines BOOLEAN NOT NULL DEFAULT false,
        difusal_hypokines BOOLEAN NOT NULL DEFAULT false,
        distol_disfunction BOOLEAN NOT NULL DEFAULT false,
        valvular_lesions BOOLEAN NOT NULL DEFAULT false,
        anevrizma BOOLEAN NOT NULL DEFAULT false,
        note TEXT
    );
    """
    )


def downgrade():
    op.execute(
        """
    DROP TABLE public.appointment_block_ekgs;
    """
    )
