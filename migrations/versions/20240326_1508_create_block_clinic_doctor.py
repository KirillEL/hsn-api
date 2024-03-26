"""create_block_clinic_doctor

Revision ID: b977397a4d79
Revises: da19609011a8
Create Date: 2024-03-26 15:08:54.480290

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b977397a4d79'
down_revision: Union[str, None] = 'da19609011a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.appointment_block_clinic_doctors (
    id integer constraint appointment_block_clinic_doctor_id_pk primary key,
    referring_doctor text,
    referring_clinic_organization text,
    disability varchar(50) not null default 'нет',
    lgota_drugs varchar(50) not null default 'нет',
    has_hospitalization boolean not null default false,
    count_hospitalization integer,
    last_hospitalization_date timestamp without time zone
    );
    ''')


def downgrade() -> None:
    op.execute('drop table public.appointment_block_clinic_doctors;')

