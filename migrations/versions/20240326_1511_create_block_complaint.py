"""create_block_complaint

Revision ID: 72e38a033c20
Revises: bf13a3cfcbc5
Create Date: 2024-03-26 15:11:20.632730

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "72e38a033c20"
down_revision: Union[str, None] = "6525415a6f99"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        """
    CREATE TABLE public.appointment_block_complaints (
        id SERIAL PRIMARY KEY,
        has_fatigue BOOLEAN NOT NULL DEFAULT false,
        has_dyspnea BOOLEAN NOT NULL DEFAULT false,
        increased_ad boolean not null default false,
        rapid_heartbeat boolean not null default false,
        has_swelling_legs BOOLEAN NOT NULL DEFAULT false,
        has_weakness BOOLEAN NOT NULL DEFAULT false,
        has_orthopnea BOOLEAN NOT NULL DEFAULT false,
        note TEXT
    );
    """
    )


def downgrade():
    op.execute(
        """
    DROP TABLE public.appointment_block_complaints;
    """
    )
