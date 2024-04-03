"""contragents

Revision ID: aa7ba3ee650a
Revises: ebae5f304ca1
Create Date: 2024-02-24 10:37:56.234279

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa7ba3ee650a'
down_revision: Union[str, None] = 'f88e9bd5c2dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.contragents (
    id serial constraint contragents_pk primary key,
    name varchar(255) not null,
    last_name varchar(255) not null,
    patronymic varchar(255),
    birth_date varchar(255) not null,
    dod varchar(255)
    );
    ''')


def downgrade() -> None:
    op.execute('drop table public.contragents;')
