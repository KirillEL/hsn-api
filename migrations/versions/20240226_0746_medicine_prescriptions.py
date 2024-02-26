"""medicine_prescriptions

Revision ID: f3f9d47b1f01
Revises: 400249a20df2
Create Date: 2024-02-26 07:46:01.325501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3f9d47b1f01'
down_revision: Union[str, None] = '400249a20df2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.medicine_prescriptions (
    id serial constraint medicine_prescription_pk primary key,
    medicine_group_id integer not null constraint medicine_prescription_medicine_group_fk
        references public.medicines_group,
    patient_appointment_id integer not null constraint medicine_prescription_patient_appointment_fk
        references public.patient_appointments,
    
    name text not null,
    mnn varchar(200),
    dosa integer not null,
    
    note text,
    
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
            create trigger medicine_prescription_updated_at_trg
            before update
            on public.medicine_prescriptions
            for each row
            execute procedure base.set_updated_at();
            ''')

    op.execute('''
                create trigger medicine_prescription_deleted_at_trg
                before update
                on public.medicine_prescriptions
                for each row
                execute procedure base.set_deleted_at();
                ''')


def downgrade() -> None:
    op.execute('drop trigger medicine_prescription_updated_at_trg on public.medicine_prescriptions;')
    op.execute('drop trigger medicine_prescription_deleted_at_trg on public.medicine_prescriptions;')
    op.execute('drop table public.medicine_prescriptions;')
