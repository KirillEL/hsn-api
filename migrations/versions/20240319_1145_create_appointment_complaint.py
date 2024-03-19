"""create appointment complaint

Revision ID: 94d7a99f5b44
Revises: da19609011a8
Create Date: 2024-03-19 11:45:32.704320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94d7a99f5b44'
down_revision: Union[str, None] = 'da19609011a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.appointment_complaints (
    id serial constraint appointment_complaint_pk
        primary key,
    has_fatigue boolean not null default false,
    has_dyspnea boolean not null default false,
    has_swelling_legs boolean not null default false,
    has_weakness boolean not null default false,
    has_orthopnea boolean not null default false,
    has_heartbeat boolean not null default true,
    note_complaints text,
    note_clinical text,
    note_ekg text,
    date_ekg timestamp without time zone,
    date_echo_ekg timestamp without time zone,
    fraction_out float not null,
    sdla float not null
    );
    ''')


def downgrade() -> None:
    op.execute('drop table public.appointment_complaints;')

