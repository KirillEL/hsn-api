"""update med_prescription

Revision ID: 5bff84352455
Revises: 16bd1557ccb3
Create Date: 2024-09-17 03:46:02.923040

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bff84352455'
down_revision: Union[str, None] = '16bd1557ccb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    ALTER TABLE public.medicine_prescriptions ADD COLUMN IF NOT EXISTS
    appointment_purpose_id bigint constraint med_prescription_purpose_id_fk
                references public.appointment_purposes not null;
    ''')




def downgrade() -> None:
    op.execute('''
    ALTER TABLE public.medicine_prescriptions DROP COLUMN IF EXISTS appointment_purpose_id;
    ''')
