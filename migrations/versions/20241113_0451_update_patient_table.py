"""update patient table

Revision ID: 47d441c7a9e9
Revises: 2639d6fa7326
Create Date: 2024-11-13 04:51:28.192779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47d441c7a9e9'
down_revision: Union[str, None] = '2639d6fa7326'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.execute('''
    ALTER TABLE public.patients
    ADD COLUMN referring_doctor text;
    ''')
    op.execute('''
    ALTER TABLE public.patients
    ADD COLUMN referring_clinic_organization text;
    ''')
    op.execute('''
    ALTER TABLE public.patients
    ADD COLUMN disability varchar(50) not null default 'нет';
    ''')
    op.execute('''
    ALTER TABLE public.patients
    ADD COLUMN lgota_drugs varchar(50) not null default 'нет';
    ''')

    op.execute('''
    ALTER TABLE public.patients
    ADD COLUMN has_hospitalization bool default false;
    ''')
    op.execute('''
    ALTER TABLE public.patients
    ADD COLUMN count_hospitalization integer;
    ''')
    op.execute('''
    ALTER TABLE public.patients
    ADD COLUMN last_hospitalization_date text;
    ''')


def downgrade() -> None:
    op.execute('''
    ALTER TABLE public.patients
    DROP COLUMN IF EXISTS last_hospitalization_date;
    ''')
    op.execute('''
    ALTER TABLE public.patients
    DROP COLUMN IF EXISTS count_hospitalization;
    ''')
    op.execute('''
        ALTER TABLE public.patients
        DROP COLUMN IF EXISTS has_hospitalization;
    ''')
    op.execute('''
        ALTER TABLE public.patients
        DROP COLUMN IF EXISTS lgota_drugs;
        ''')
    op.execute('''
        ALTER TABLE public.patients
        DROP COLUMN IF EXISTS disability;
        ''')
    op.execute('''
        ALTER TABLE public.patients
        DROP COLUMN IF EXISTS referring_clinic_organization;
        ''')
    op.execute('''
        ALTER TABLE public.patients
        DROP COLUMN IF EXISTS referring_doctor;
        ''')
