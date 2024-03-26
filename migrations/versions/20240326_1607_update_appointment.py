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
down_revision: Union[str, None] = '8a1dbf4423b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    def upgrade():
        # Добавление новых столбцов
        op.execute('''
        ALTER TABLE public.appointments
        ADD COLUMN block_clinic_doctor_id INTEGER NOT NULL;
        ''')
        op.execute('''
        ALTER TABLE public.appointments
        ADD COLUMN block_diagnose_id INTEGER NOT NULL;
        ''')
        op.execute('''
        ALTER TABLE public.appointments
        ADD COLUMN block_laboratory_test_id INTEGER NOT NULL;
        ''')
        op.execute('''
        ALTER TABLE public.appointments
        ADD COLUMN block_ekg_id INTEGER NOT NULL;
        ''')
        op.execute('''
        ALTER TABLE public.appointments
        ADD COLUMN block_complaint_id INTEGER NOT NULL;
        ''')
        op.execute('''
        ALTER TABLE public.appointments
        ADD COLUMN block_clinical_condition_id INTEGER NOT NULL;
        ''')
        op.execute('''
        ALTER TABLE public.appointments
        ADD COLUMN block_drug_therapy_id INTEGER NOT NULL;
        ''')

        # Добавление ограничений внешнего ключа
        op.execute('''
        ALTER TABLE public.appointment_block_ekgs
        ADD CONSTRAINT fk_block_clinic_doctor FOREIGN KEY (block_clinic_doctor_id)
            REFERENCES public.appointment_block_clinic_doctors(id);
        ''')
        op.execute('''
        ALTER TABLE public.appointment_block_ekgs
        ADD CONSTRAINT fk_block_diagnose FOREIGN KEY (block_diagnose_id)
            REFERENCES public.appointment_block_diagnoses(id);
        ''')
        op.execute('''
        ALTER TABLE public.appointment_block_ekgs
        ADD CONSTRAINT fk_block_laboratory_test FOREIGN KEY (block_laboratory_test_id)
            REFERENCES public.appointment_block_laboratory_tests(id);
        ''')
        op.execute('''
        ALTER TABLE public.appointment_block_ekgs
        ADD CONSTRAINT fk_block_ekg FOREIGN KEY (block_ekg_id)
            REFERENCES public.appointment_block_ekgs(id);
        ''')
        op.execute('''
        ALTER TABLE public.appointment_block_ekgs
        ADD CONSTRAINT fk_block_complaint FOREIGN KEY (block_complaint_id)
            REFERENCES public.appointment_block_complaints(id);
        ''')
        op.execute('''
        ALTER TABLE public.appointment_block_ekgs
        ADD CONSTRAINT fk_block_clinical_condition FOREIGN KEY (block_clinical_condition_id)
            REFERENCES public.appointment_block_clinical_conditions(id);
        ''')
        op.execute('''
        ALTER TABLE public.appointment_block_ekgs
        ADD CONSTRAINT fk_block_drug_therapy FOREIGN KEY (block_drug_therapy_id)
            REFERENCES public.appointment_block_drug_therapies(id);
        ''')

def downgrade():
    # Команды для удаления столбцов и внешних ключей с явными именами ограничений
    op.execute("""
    ALTER TABLE public.appointment_block_ekgs
    DROP CONSTRAINT IF EXISTS fk_block_clinic_doctor,
    DROP CONSTRAINT IF EXISTS fk_block_diagnose,
    DROP CONSTRAINT IF EXISTS fk_block_laboratory_test,
    DROP CONSTRAINT IF EXISTS fk_block_ekg,
    DROP CONSTRAINT IF EXISTS fk_block_complaint,
    DROP CONSTRAINT IF EXISTS fk_block_clinical_condition,
    DROP CONSTRAINT IF EXISTS fk_block_drug_therapy;

    ALTER TABLE public.appointment_block_ekgs
    DROP COLUMN IF EXISTS block_clinic_doctor_id,
    DROP COLUMN IF EXISTS block_diagnose_id,
    DROP COLUMN IF EXISTS block_laboratory_test_id,
    DROP COLUMN IF EXISTS block_ekg_id,
    DROP COLUMN IF EXISTS block_complaint_id,
    DROP COLUMN IF EXISTS block_clinical_condition_id,
    DROP COLUMN IF EXISTS block_drug_therapy_id;
    """)
