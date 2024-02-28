"""diagnoses_catalog

Revision ID: e1bb6147cced
Revises: 9b18add210ff
Create Date: 2024-02-23 14:38:12.292630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1bb6147cced'
down_revision: Union[str, None] = '9b18add210ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.diagnoses_catalog (
    id serial constraint diagnoses_catalog_pk primary key,
    name varchar(255) not null,
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
    create trigger diagnoses_catalog_updated_at_trg
    before update
    on public.diagnoses_catalog
    for each row
    execute procedure base.set_updated_at();
    ''')

    op.execute('''
        create trigger diagnoses_catalog_deleted_at_trg
        before update
        on public.diagnoses_catalog
        for each row
        execute procedure base.set_deleted_at();
        ''')


def downgrade() -> None:
    op.execute('drop trigger diagnoses_catalog_updated_at_trg on public.diagnoses_catalog;')
    op.execute('drop trigger diagnoses_catalog_deleted_at_trg on public.diagnoses_catalog;')
    op.execute('drop table public.diagnoses_catalog;')
