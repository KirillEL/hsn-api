"""add last hospitalization id

Revision ID: 6a7266ab0f27
Revises: da19609011a8
Create Date: 2024-03-07 11:30:31.301433

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a7266ab0f27'
down_revision: Union[str, None] = 'da19609011a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    alter table public.patients add last_hospitalization_id integer constraint patient_last_hospitalization_fk
        references public.patient_hospitalizations ON DELETE SET NULL;
    ''')


def downgrade() -> None:
    op.execute('''
    alter table public.patients drop column last_hospitalization_id;
    ''')
