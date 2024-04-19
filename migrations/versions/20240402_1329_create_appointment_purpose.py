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
    dosa varchar(100) not null,
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
                    create trigger appointment_purpose_updated_at_trg
                    before update
                    on public.appointment_purposes
                    for each row
                    execute procedure base.set_updated_at();
                    ''')

    op.execute('''
                        create trigger appointment_purpose_deleted_at_trg
                        before update
                        on public.appointment_purposes
                        for each row
                        execute procedure base.set_deleted_at();
                        ''')


def downgrade() -> None:
    op.execute('drop trigger if exists appointment_purpose_updated_at_trg on public.appointment_purposes;')
    op.execute('drop trigger if exists appointment_purpose_deleted_at_trg on public.appointment_purposes;')
    op.execute('drop table if exists public.appointment_purposes;')
