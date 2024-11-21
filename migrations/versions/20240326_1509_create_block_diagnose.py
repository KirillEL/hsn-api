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
    cardiomyopathy_note varchar(40),
    ibc_pikc boolean not null default false,
    ibc_pikc_note varchar(40),
    ibc_stenocardia_napr boolean not null default false,
    ibc_stenocardia_napr_note varchar(40),
    ibc_another boolean not null default false,
    ibc_another_note varchar(40),
    fp_tp boolean not null default false,
    fp_tp_note varchar(40),
    ad boolean not null default false,
    ad_note varchar(40),
    dislipidemia boolean not null default false,
    dislipidemia_note varchar(40),
    hobl_ba boolean not null default false,
    hobl_ba_note varchar(40),
    onmk_tia boolean not null default false,
    onmk_tia_note varchar(40),
    hbp boolean not null default false,
    hbp_note varchar(40),
    another boolean not null default false,
    another_note text
    );
    """
    )


def downgrade() -> None:
    op.execute("drop table public.appointment_block_diagnoses;")
