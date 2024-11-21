"""add drug to med_prescription


Revision ID: 9cebace410bd
Revises: fac65c87b310
Create Date: 2024-09-17 07:10:50.459612

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9cebace410bd"
down_revision: Union[str, None] = "fac65c87b310"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
           ALTER TABLE public.medicine_prescriptions ADD COLUMN IF NOT EXISTS
           drug_id bigint references public.drugs ON DELETE CASCADE;
           """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE public.medicine_prescriptions DROP COLUMN IF EXISTS
        drug_id;
        """
    )
