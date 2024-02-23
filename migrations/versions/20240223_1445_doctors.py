"""doctors

Revision ID: f88e9bd5c2dc
Revises: e1bb6147cced
Create Date: 2024-02-23 14:45:00.608073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f88e9bd5c2dc'
down_revision: Union[str, None] = 'e1bb6147cced'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.doctors (
    id serial constraint doctors_pk primary key,
    name varchar(100) not null,
    last_name varchar(100) not null,
    patronymic varchar(100),
    phone_number BIGINT not null unique,
    user_id integer not null unique constraint doctors_user_fk
        references public.users,
    cabinet_id integer not null constraint doctors_cabinet_fk
        references public.cabinets,
    is_glav boolean default false not null,
    
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
        create trigger doctors_updated_at_trg
        before update
        on public.doctors
        for each row
        execute procedure base.set_updated_at();
        ''')

    op.execute('''
            create trigger doctors_deleted_at_trg
            before update
            on public.doctors
            for each row
            execute procedure base.set_deleted_at();
            ''')


def downgrade() -> None:
    op.execute('drop trigger doctors_updated_at_trg on public.doctors;')
    op.execute('drop trigger doctors_deleted_at_trg on public.doctors;')
    op.execute('drop table public.doctors;')
