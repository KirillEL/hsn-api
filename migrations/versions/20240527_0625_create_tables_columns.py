"""create tables columns

Revision ID: 6fb24123b56a
Revises: b11844181666
Create Date: 2024-05-27 06:25:44.157460

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6fb24123b56a"
down_revision: Union[str, None] = "b11844181666"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
    create table public.patient_columns (
    id serial constraint patient_columns_pk PRIMARY KEY,
    user_id integer not null unique constraint patient_columns_user_id_fk references public.users,
    table_columns jsonb not null
    );
    """
    )

    op.execute(
        """
    create table public.appointment_columns (
    id serial constraint appointment_columns_pk PRIMARY KEY,
    user_id integer not null unique constraint appointment_columns_user_id_fk references public.users,
    table_columns jsonb not null
    );
    """
    )


def downgrade() -> None:
    op.execute("drop table if exists public.appointment_columns;")
    op.execute("drop table if exists public.patient_columns;")
