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

    op.execute('''
    CREATE TYPE gender_type AS ENUM ('male', 'female');
    ''')

    op.execute('''
    CREATE TYPE disability_type AS ENUM ('no', 'first', 'second', 'third');
    ''')

    op.execute('''
    CREATE TYPE lgota_drugs_type AS ENUM ('no', 'yes', 'money');
    ''')

    op.execute('''
    CREATE TYPE classification_func_classes_type AS ENUM ('fk1', 'fk2', 'fk3', 'fk4');
    ''')

    op.execute('''
    CREATE TYPE classification_adjacent_release_type AS ENUM ('<40', '40-49', '>50');
    ''')

    op.execute('''
    CREATE TYPE distance_walking_type AS ENUM ('<200', '200-350', '350-500', '>500');
    ''')

    op.execute('''
    CREATE TYPE classification_nc_stage_type AS ENUM ('IA', 'IB', 'IIA', 'IIB', 'IIIA', 'IIIB');
    ''')



def downgrade() -> None:
    op.execute('drop function base.set_updated_at();')
    op.execute('drop function base.set_deleted_at();')
    op.execute('drop schema base;')
    op.execute('drop type classification_func_classes_type;')
    op.execute('drop type lgota_drugs_type;')
    op.execute('drop type disability_type;')
    op.execute('drop type gender_type;')

