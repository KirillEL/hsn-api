"""researchs

Revision ID: 006f92681953
Revises: 462667f47011
Create Date: 2024-02-26 07:47:52.028567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '006f92681953'
down_revision: Union[str, None] = '462667f47011'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.researchs (
    id serial constraint research_pk primary key,
    analise_id integer not null constraint research_analise_fk
        references public.analises,
    patient_appointment_id integer not null constraint research_patient_appointment_fk
        references public.patient_appointments,
    patient_hospitalization_id integer not null constraint research_patient_hospitalization_fk
        references public.patient_hospitalizations,
        
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
            create trigger research_updated_at_trg
            before update
            on public.researchs
            for each row
            execute procedure base.set_updated_at();
            ''')

    op.execute('''
                create trigger research_deleted_at_trg
                before update
                on public.researchs
                for each row
                execute procedure base.set_deleted_at();
                ''')


def downgrade() -> None:
    op.execute('drop trigger research_updated_at_trg on public.researchs;')
    op.execute('drop trigger research_deleted_at_trg on public.researchs;')
    op.execute('drop table public.researchs;')
