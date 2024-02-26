"""patient_hospitalizations

Revision ID: 7872038b4a6f
Revises: f3f9d47b1f01
Create Date: 2024-02-26 07:46:50.270974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7872038b4a6f'
down_revision: Union[str, None] = 'f3f9d47b1f01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.patient_hospitalizations (
    id serial constraint patient_hospitalization_pk primary key,
    patient_id integer not null constraint patient_hospitalization_patient_fk
        references public.patients,
    date_start timestamp with time zone not null,
    date_end timestamp with time zone not null,
    
    anamnes text,
    
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
            create trigger patient_hospitalization_updated_at_trg
            before update
            on public.patient_hospitalizations
            for each row
            execute procedure base.set_updated_at();
            ''')

    op.execute('''
                create trigger patient_hospitalization_deleted_at_trg
                before update
                on public.patient_hospitalizations
                for each row
                execute procedure base.set_deleted_at();
                ''')


def downgrade() -> None:
    op.execute('drop trigger patient_hospitalization_updated_at_trg on public.patient_hospitalizations;')
    op.execute('drop trigger patient_hospitalization_deleted_at_trg on public.patient_hospitalizations;')
    op.execute('drop table public.patient_hospitalizations;')

