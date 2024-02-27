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
        references public.cabinets,
    name varchar(255) not null,
    last_name varchar(255) not null,
    patronymic varchar(255),
    gender gender_type,
    height integer not null,
    age integer not null,
    main_diagnose text,
    disability disability_type not null default 'no',
    
    date_setup_diagnose timestamp with time zone not null,
    school_hsn_date timestamp with time zone,
    
    lgota_drugs lgota_drugs_type not null default 'no',
    classification_func_classes classification_func_classes_type not null default 'fk1',
    
    note text,
    
    has_chronic_heart boolean not null default false,
    has_stenocardia boolean not null default false,
    has_arteria_hypertension boolean not null default false,
    
    arteria_hypertension_age integer,
    
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
