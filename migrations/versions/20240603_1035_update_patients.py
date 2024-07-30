"""update patients

Revision ID: 16bd1557ccb3
Revises: 6fb24123b56a
Create Date: 2024-06-03 10:35:30.869281

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "16bd1557ccb3"
down_revision: Union[str, None] = "6fb24123b56a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
    ALTER TABLE public.patients ADD COLUMN IF NOT EXISTS referring_doctor text;
    """
    )

    op.execute(
        """
    ALTER TABLE public.patients ADD COLUMN IF NOT EXISTS referring_clinic_organization text;
    """
    )

    op.execute(
        """
    ALTER TABLE public.patients ADD COLUMN IF NOT EXISTS disability varchar(50) not null default 'нет';
    """
    )

    op.execute(
        """
    ALTER TABLE public.patients ADD COLUMN IF NOT EXISTS lgota_drugs varchar(50) not null default 'нет';
    """
    )

    op.execute(
        """
    ALTER TABLE public.patients ADD COLUMN IF NOT EXISTS has_hospitalization boolean not null default false;
    """
    )

    op.execute(
        """
    ALTER TABLE public.patients ADD COLUMN IF NOT EXISTS count_hospitalization integer;
    """
    )

    op.execute(
        """
    ALTER TABLE public.patients ADD COLUMN IF NOT EXISTS last_hospitalization_date text;
    """
    )


def downgrade() -> None:
    op.drop_column("public.patients", "last_hospitalization_date")
    op.drop_column("public.patients", "count_hospitalization")
    op.drop_column("public.patients", "has_hospitalization")
    op.drop_column("public.patients", "lgota_drugs")
    op.drop_column("public.patients", "disability")
    op.drop_column("public.patients", "referring_clinic_organization")
    op.drop_column("public.patients", "referring_doctor")
