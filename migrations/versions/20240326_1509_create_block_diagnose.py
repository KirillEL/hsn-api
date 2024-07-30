"""create_block_diagnose

Revision ID: 2318f2994dcf
Revises: b977397a4d79
Create Date: 2024-03-26 15:09:34.691093

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2318f2994dcf"
down_revision: Union[str, None] = "b977397a4d79"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
    create table public.appointment_block_diagnoses (
    id serial constraint appointment_block_diagnose_id_pk primary key,
    diagnose text not null,
    classification_func_classes varchar(1) not null,
    classification_adjacent_release varchar(50) not null,
    classification_nc_stage varchar(5) not null,
    cardiomyopathy boolean not null default false,
    cardiomyopathy_note text,
    ibc_pikc boolean not null default false,
    ibc_pikc_note text,
    ibc_stenocardia_napr boolean not null default false,
    ibc_stenocardia_napr_note text,
    ibc_another boolean not null default false,
    ibc_another_note text,
    fp_tp boolean not null default false,
    fp_tp_note text,
    ad boolean not null default false,
    ad_note text,
    cd boolean not null default false,
    cd_note text,
    hobl_ba boolean not null default false,
    hobl_ba_note text,
    onmk_tia boolean not null default false,
    onmk_tia_note text,
    hbp boolean not null default false,
    hbp_note text,
    another text
    );
    """
    )


def downgrade() -> None:
    op.execute("drop table public.appointment_block_diagnoses;")
