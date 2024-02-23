"""cabinets

Revision ID: 9b18add210ff
Revises: 76c177bcb84c
Create Date: 2024-02-23 14:23:47.648568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b18add210ff'
down_revision: Union[str, None] = '76c177bcb84c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.cabinets (
    id serial constraint cabinets_pk primary key,
    number varchar(255) NOT NULL,
    med_id integer not null constraint cabinets_med_fk references public.med_organizations,
    
    created_at   timestamp with time zone default now() not null,
    created_by   integer not null,

    updated_at   timestamp with time zone,
    updated_by   integer,

    deleted_at   timestamp with time zone,
    deleted_by   integer
    );
    ''')

    op.execute('''
        create trigger cabinets_updated_at_trg
        before update
        on public.cabinets
        for each row
        execute procedure base.set_updated_at();
        ''')

    op.execute('''
            create trigger cabinets_deleted_at_trg
            before update
            on public.cabinets
            for each row
            execute procedure base.set_deleted_at();
            ''')


def downgrade() -> None:
    op.execute('drop trigger cabinets_updated_at_trg on public.cabinets;')
    op.execute('drop trigger cabinets_deleted_at_trg on public.cabinets;')
    op.execute('drop table public.cabinets;')
