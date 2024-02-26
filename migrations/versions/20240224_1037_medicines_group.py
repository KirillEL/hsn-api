"""medicines_group

Revision ID: ebae5f304ca1
Revises: f88e9bd5c2dc
Create Date: 2024-02-24 10:37:45.445250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebae5f304ca1'
down_revision: Union[str, None] = 'f88e9bd5c2dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.medicines_group (
    id serial constraint medicines_group_pk primary key,
    code varchar(50) UNIQUE NOT NULL,
    name varchar(255) NOT NULL,
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
            create trigger medicines_group_updated_at_trg
            before update
            on public.medicines_group
            for each row
            execute procedure base.set_updated_at();
            ''')

    op.execute('''
                create trigger medicines_group_deleted_at_trg
                before update
                on public.medicines_group
                for each row
                execute procedure base.set_deleted_at();
                ''')


def downgrade() -> None:
    op.execute('drop trigger medicines_group_updated_at_trg on public.medicines_group;')
    op.execute('drop trigger medicines_group_deleted_at_trg on public.medicines_group;')
    op.execute('drop table public.medicines_group;')
