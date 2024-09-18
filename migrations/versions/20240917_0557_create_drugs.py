"""create drugs

Revision ID: fac65c87b310
Revises: 5bff84352455
Create Date: 2024-09-17 05:57:04.520088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'fac65c87b310'
down_revision: Union[str, None] = '5bff84352455'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    CREATE TABLE public.drug_groups (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            is_deleted BOOLEAN NOT NULL DEFAULT false,
            created_at TIMESTAMP NOT NULL DEFAULT now(),
            updated_at TIMESTAMP,
            deleted_at TIMESTAMP,
            created_by INTEGER NOT NULL,
            updated_by INTEGER,
            deleted_by INTEGER
        );
    ''')

    op.execute('''
    create trigger drug_group_updated_at_trg
    before update
    on public.drug_groups
    for each row
    execute procedure base.set_updated_at();
    ''')

    op.execute('''
    create trigger drug_group_deleted_at_trg
    before update
    on public.drug_groups
    for each row
    execute procedure base.set_deleted_at();
    ''')

    op.execute("""
            CREATE TABLE public.drugs (
                id BIGSERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                drug_group_id BIGINT REFERENCES public.drug_groups(id) ON DELETE CASCADE,
                is_deleted BOOLEAN NOT NULL DEFAULT false
            );
        """)


def downgrade() -> None:
    op.execute('drop table if exists public.drugs;')
    op.execute('drop trigger if exists drug_group_updated_at_trg on public.drug_groups;')
    op.execute('drop trigger if exists drug_group_deleted_at_trg on public.drug_groups;')
    op.execute('drop table if exists public.drug_groups;')
