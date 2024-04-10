"""create appointment function and trigger to update status

Revision ID: b11844181666
Revises: 3834df9dfd04
Create Date: 2024-04-10 20:27:49.520989

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b11844181666'
down_revision: Union[str, None] = '3834df9dfd04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    CREATE OR REPLACE FUNCTION base.check_appointment_completion()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.block_clinic_doctor_id IS NOT NULL AND
       NEW.block_diagnose_id IS NOT NULL AND
       NEW.block_laboratory_test_id IS NOT NULL AND
       NEW.block_ekg_id IS NOT NULL AND
       NEW.block_complaint_id IS NOT NULL AND
       NEW.block_clinical_condition_id IS NOT NULL THEN
        NEW.status = 'completed'::public.appointmentstatus;
    ELSE
        NEW.status = 'progress'::public.appointmentstatus;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
    ''')

    op.execute('''
    CREATE TRIGGER trigger_check_appointment_completion
BEFORE INSERT OR UPDATE ON public.appointments
FOR EACH ROW EXECUTE FUNCTION base.check_appointment_completion();
    ''')


def downgrade() -> None:
    op.execute('DROP TRIGGER IF EXISTS trigger_check_appointment_completion ON public.appointments;')

    # Удаление функции
    op.execute('DROP FUNCTION IF EXISTS base.check_appointment_completion();')

