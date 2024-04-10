"""add status to appointment

Revision ID: 3834df9dfd04
Revises: ed6c25991933
Create Date: 2024-04-10 20:22:26.023630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3834df9dfd04'
down_revision: Union[str, None] = 'ed6c25991933'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE TYPE public.appointmentstatus AS ENUM('progress', 'completed')")

    op.execute("ALTER TABLE public.appointments ADD COLUMN status public.appointmentstatus NOT NULL DEFAULT 'progress'")


def downgrade() -> None:
    op.execute("ALTER TABLE public.appointments DROP COLUMN status")


    op.execute("DROP TYPE public.appointmentstatus")
