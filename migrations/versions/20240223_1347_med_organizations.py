"""med_organizations

Revision ID: c9c032fedc0f
Revises: c1ba7eec30e7
Create Date: 2024-02-23 13:47:38.332662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9c032fedc0f'
down_revision: Union[str, None] = 'c1ba7eec30e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.med_organizations
    (
    id serial constraint med_organizations_pk primary key,
    name varchar(255) NOT NULL,
    number integer UNIQUE NOT NULL,
    address text NOT NULL,

    is_deleted boolean DEFAULT false NOT NULL,

    created_at timestamp with time zone DEFAULT now() NOT NULL,
    created_by integer,

    updated_at timestamp with time zone,
    updated_by integer,

    deleted_at timestamp with time zone,
    deleted_by integer
    );
    ''')

    op.execute('''
    create trigger med_organization_updated_at_trg
    before update
    on public.med_organizations
    for each row
    execute procedure base.set_updated_at();
    ''')

    op.execute('''
       create trigger med_organization_deleted_at_trg
       before update
       on public.med_organizations
       for each row
       execute procedure base.set_deleted_at();
       ''')


def downgrade() -> None:
    op.execute('drop trigger med_organization_updated_at_trg on public.med_organizations;')
    op.execute('drop trigger med_organization_deleted_at_trg on public.med_organizations;')
    op.execute('drop table public.med_organizations;')