"""update appointment

Revision ID: d5e77ddf7bf4
Revises: 8a1dbf4423b2
Create Date: 2024-03-26 16:07:06.165765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd5e77ddf7bf4'
down_revision: Union[str, None] = 'bf13a3cfcbc5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Добавление новых столбцов
    op.execute('''
        ALTER TABLE public.appointments
        ADD COLUMN block_clinic_doctor_id INTEGER;
        ''')
    op.execute('''
        ALTER TABLE public.appointments
        ADD COLUMN block_diagnose_id INTEGER;
        ''')
    op.execute('''
        ALTER TABLE public.appointments
        ADD COLUMN block_laboratory_test_id INTEGER;
        ''')
    op.execute('''
        ALTER TABLE public.appointments
        ADD COLUMN block_ekg_id INTEGER;
        ''')
    op.execute('''
        ALTER TABLE public.appointments
        ADD COLUMN block_complaint_id INTEGER;
        ''')
    op.execute('''
        ALTER TABLE public.appointments
        ADD COLUMN block_clinical_condition_id INTEGER;
        ''')

    # Добавление ограничений внешнего ключа
    op.execute('''
        ALTER TABLE public.appointments
        ADD CONSTRAINT fk_block_clinic_doctor FOREIGN KEY (block_clinic_doctor_id)
            REFERENCES public.appointment_block_clinic_doctors(id);
        ''')
    op.execute('''
        ALTER TABLE public.appointments
        ADD CONSTRAINT fk_block_diagnose FOREIGN KEY (block_diagnose_id)
            REFERENCES public.appointment_block_diagnoses(id);
        ''')
    op.execute('''
        ALTER TABLE public.appointments
        ADD CONSTRAINT fk_block_laboratory_test FOREIGN KEY (block_laboratory_test_id)
            REFERENCES public.appointment_block_laboratory_tests(id);
        ''')
    op.execute('''
        ALTER TABLE public.appointments
        ADD CONSTRAINT fk_block_ekg FOREIGN KEY (block_ekg_id)
            REFERENCES public.appointment_block_ekgs(id);
        ''')
    op.execute('''
        ALTER TABLE public.appointments
        ADD CONSTRAINT fk_block_complaint FOREIGN KEY (block_complaint_id)
            REFERENCES public.appointment_block_complaints(id);
        ''')
    op.execute('''
        ALTER TABLE public.appointments
        ADD CONSTRAINT fk_block_clinical_condition FOREIGN KEY (block_clinical_condition_id)
            REFERENCES public.appointment_block_clinical_conditions(id);
        ''')
    

def downgrade():
    op.execute('''
    ALTER TABLE public.appointments
    DROP CONSTRAINT IF EXISTS fk_block_clinic_doctor;
    ''')

    op.execute('''
    ALTER TABLE public.appointments
    DROP CONSTRAINT IF EXISTS fk_block_diagnose;
        ''')

    op.execute('''
        ALTER TABLE public.appointments
        DROP CONSTRAINT IF EXISTS fk_block_laboratory_test;
            ''')

    op.execute('''
        ALTER TABLE public.appointments
        DROP CONSTRAINT IF EXISTS fk_block_ekg;
            ''')

    op.execute('''
        ALTER TABLE public.appointments
        DROP CONSTRAINT IF EXISTS fk_block_complaint;
            ''')

    op.execute('''
        ALTER TABLE public.appointments
        DROP CONSTRAINT IF EXISTS fk_block_clinical_condition;
            ''')

    op.execute('''
    ALTER TABLE public.appointments
    DROP COLUMN IF EXISTS block_clinic_doctor_id;
    ''')
    op.execute('''
    ALTER TABLE public.appointments
    DROP COLUMN IF EXISTS block_diagnose_id;
        ''')

    op.execute('''
    ALTER TABLE public.appointments
    DROP COLUMN IF EXISTS block_laboratory_test_id;
        ''')

    op.execute('''
    ALTER TABLE public.appointments
    DROP COLUMN IF EXISTS block_ekg_id;
        ''')

    op.execute('''
    ALTER TABLE public.appointments
    DROP COLUMN IF EXISTS block_complaint_id;
        ''')

    op.execute('''
    ALTER TABLE public.appointments
    DROP COLUMN IF EXISTS block_clinical_condition_id;
        ''')
