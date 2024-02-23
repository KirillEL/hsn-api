"""base

Revision ID: 9e845d5c5eab
Revises: 
Create Date: 2024-02-23 13:47:09.915188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e845d5c5eab'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('create schema base;')
    op.execute('''
    create function base.set_updated_at() returns trigger
        language plpgsql
    as
    $$DECLARE
        _NEW record;
        BEGIN
        _NEW := NEW;
        _NEW.updated_at = now();
        RETURN _NEW;
        END;
    $$;
    ''')

    op.execute('''
        create function base.set_deleted_at() returns trigger
            language plpgsql
        as
        $$
        DECLARE
              _NEW record;
            BEGIN
                _NEW := NEW;

                if OLD.is_deleted is false and _NEW.is_deleted then
                    _NEW.deleted_at = now();
                end if;

                RETURN _NEW;
            END;
        $$;
            ''')


def downgrade() -> None:
    op.execute('drop function base.set_updated_at();')
    op.execute('drop function base.set_deleted_at();')
    op.execute('drop schema base;')