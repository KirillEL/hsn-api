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
down_revision: Union[str, None] = 'ebae5f304ca1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.contragents (
    id serial constraint contragents_pk primary key,
    phone_number text not null unique,
    address text not null,
    snils text not null unique,
    mis_number text not null,
    date_birth text not null,
    relative_phone_number text,
    parent text,
    date_dead text
    );
    ''')


def downgrade() -> None:
    op.execute('drop table public.contragents;')
