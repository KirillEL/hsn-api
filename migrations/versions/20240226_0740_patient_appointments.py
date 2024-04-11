"""patient_appointments

Revision ID: 94cef94d62e8
Revises: 133bc396df29
Create Date: 2024-02-26 07:40:29.945237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94cef94d62e8'
down_revision: Union[str, None] = '133bc396df29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.appointments (
    id serial constraint patient_appointments_pk primary key,
    doctor_id integer not null constraint appointment_doctor_id_fk
        references public.doctors,
    patient_id integer not null constraint appointment_patient_id_fk
        references public.patients,
    date text not null default to_char(current_date, 'DD.MM.YYYY'),
    date_next text,
    
    is_deleted boolean not null default false,
    
    created_at   timestamp with time zone default now() not null,
    created_by   integer not null,

    updated_at   timestamp with time zone,
    updated_by   integer,

    deleted_at   timestamp with time zone,
    deleted_by   integer
    );
    ''')

    op.execute('''
            create trigger appointment_updated_at_trg
            before update
            on public.appointments
            for each row
            execute procedure base.set_updated_at();
            ''')

    op.execute('''
                create trigger appointment_deleted_at_trg
                before update
                on public.appointments
                for each row
                execute procedure base.set_deleted_at();
                ''')


def downgrade() -> None:
    op.execute('drop trigger appointment_updated_at_trg on public.appointments;')
    op.execute('drop trigger appointment_deleted_at_trg on public.appointments;')
    op.execute('drop table appointments;')


