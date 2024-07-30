"""supplied_diagnoses

Revision ID: 462667f47011
Revises: 7872038b4a6f
Create Date: 2024-02-26 07:47:27.735820

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "462667f47011"
down_revision: Union[str, None] = "006f92681953"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
    create table supplied_diagnoses (
    id serial constraint supplied_diagnose_pk primary key,
    appointment_id integer not null constraint appointment_supplied_diagnose_fk
        references public.appointments ON DELETE CASCADE,
    diagnose_catalog_id integer not null constraint supplied_diagnose_diagnose_catalog_fk
        references public.diagnoses_catalog ON DELETE CASCADE,
    medicine_prescription_id integer not null constraint supplied_diagnose_medicine_prescription_fk
        references public.medicine_prescriptions ON DELETE CASCADE,
    
    note text,
    
    is_deleted boolean not null default false,
    
    created_at   timestamp with time zone default now() not null,
    created_by   integer not null,

    updated_at   timestamp with time zone,
    updated_by   integer,

    deleted_at   timestamp with time zone,
    deleted_by   integer
    );
    """
    )

    op.execute(
        """
            create trigger supplied_diagnose_updated_at_trg
            before update
            on public.supplied_diagnoses
            for each row
            execute procedure base.set_updated_at();
            """
    )

    op.execute(
        """
                create trigger supplied_diagnose_deleted_at_trg
                before update
                on public.supplied_diagnoses
                for each row
                execute procedure base.set_deleted_at();
                """
    )


def downgrade() -> None:
    op.execute(
        "drop trigger supplied_diagnose_updated_at_trg on public.supplied_diagnoses;"
    )
    op.execute(
        "drop trigger supplied_diagnose_deleted_at_trg on public.supplied_diagnoses;"
    )
    op.execute("drop table public.supplied_diagnoses;")
