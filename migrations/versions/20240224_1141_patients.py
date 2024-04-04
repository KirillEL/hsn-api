"""patients

Revision ID: 133bc396df29
Revises: aa7ba3ee650a
Create Date: 2024-02-24 11:41:21.170811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '133bc396df29'
down_revision: Union[str, None] = 'aa7ba3ee650a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.patients (
    id serial constraint patients_pk primary key,
    contragent_id integer not null unique constraint patients_contragent_fk
        references public.contragents,
    cabinet_id integer constraint patients_cabinet_fk
        references public.cabinets ON DELETE SET NULL,
    gender varchar(1) not null,
    location varchar(255) not null,
    district varchar(255) not null,
    address varchar(255) not null,
    phone varchar(20) not null,
    clinic varchar(255) not null,
    referring_doctor varchar(255),
    referring_clinic_organization varchar(255),
    disability varchar(100) not null,
    lgota_drugs varchar(100) not null,
    has_hospitalization boolean not null default false,
    count_hospitalization integer,
    last_hospitalization_date varchar(255),
    patient_note text,
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
            create trigger patients_updated_at_trg
            before update
            on public.patients
            for each row
            execute procedure base.set_updated_at();
            ''')

    op.execute('''
                create trigger patients_deleted_at_trg
                before update
                on public.patients
                for each row
                execute procedure base.set_deleted_at();
                ''')



def downgrade() -> None:
    op.execute('drop trigger patients_updated_at_trg on public.patients;')
    op.execute('drop trigger patients_deleted_at_trg on public.patients;')
    op.execute('drop table public.patients;')
