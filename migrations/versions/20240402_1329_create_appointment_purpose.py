"""create appointment purpose

Revision ID: ed6c25991933
Revises: d5e77ddf7bf4
Create Date: 2024-04-02 13:29:52.820882

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed6c25991933'
down_revision: Union[str, None] = 'd5e77ddf7bf4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.appointment_purposes (
    id serial constraint appointment_purpose_id_pk primary key,
    appointment_id integer constraint appointment_id_fk
        references public.appointments,
    medicine_prescription_id integer constraint medicine_prescription_id_fk
        references public.medicine_prescriptions,
    note text
    );
    ''')


def downgrade() -> None:
    op.execute('drop table if exists public.appointment_purposes;')
