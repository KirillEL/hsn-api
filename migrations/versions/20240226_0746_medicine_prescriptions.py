"""medicine_prescriptions

Revision ID: f3f9d47b1f01
Revises: 400249a20df2
Create Date: 2024-02-26 07:46:01.325501

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "f3f9d47b1f01"
down_revision: Union[str, None] = "400249a20df2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        create table public.patient_hospitalizations (
        id serial constraint patient_hospitalization_pk primary key,
        patient_id integer not null constraint patient_hospitalization_patient_fk
            references public.patients ON DELETE CASCADE,
        date_start timestamp with time zone not null,
        date_end timestamp with time zone not null,

        anamnes text,

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
                create trigger patient_hospitalization_updated_at_trg
                before update
                on public.patient_hospitalizations
                for each row
                execute procedure base.set_updated_at();
                """
    )

    op.execute(
        """
                    create trigger patient_hospitalization_deleted_at_trg
                    before update
                    on public.patient_hospitalizations
                    for each row
                    execute procedure base.set_deleted_at();
                    """
    )

    op.execute(
        """
    create table public.medicines_group (
    id serial constraint medicine_group_pk primary key,
    code varchar(100),
    name varchar(255) not null,
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
                    create or replace trigger medicines_group_updated_at_trg
                    before update
                    on public.medicines_group
                    for each row
                    execute procedure base.set_updated_at();
                    """
    )

    op.execute(
        """
                        create or replace trigger medicines_group_deleted_at_trg
                        before update
                        on public.medicines_group
                        for each row
                        execute procedure base.set_deleted_at();
                        """
    )

    op.execute(
        """
        create table public.medicine_prescriptions (
            id serial constraint med_prescription_id_pk primary key,
            dosa varchar(10) not null,
            note varchar(500),

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
            create trigger medicine_prescription_updated_at_trg
            before update
            on public.medicine_prescriptions
            for each row
            execute procedure base.set_updated_at();
            """
    )

    op.execute(
        """
                create trigger medicine_prescription_deleted_at_trg
                before update
                on public.medicine_prescriptions
                for each row
                execute procedure base.set_deleted_at();
                """
    )


def downgrade() -> None:
    op.execute(
        "drop trigger if exists patient_hospitalization_updated_at_trg on public.patient_hospitalizations;"
    )
    op.execute(
        "drop trigger if exists patient_hospitalization_deleted_at_trg on public.patient_hospitalizations;"
    )
    op.execute("drop table if exists public.patient_hospitalizations CASCADE;")

    op.execute(
        "drop trigger if exists medicines_group_updated_at_trg on public.medicines_group;"
    )
    op.execute(
        "drop trigger if exists medicines_group_deleted_at_trg on public.medicines_group;"
    )
    op.execute("drop table if exists public.medicines_group CASCADE;")

    op.execute(
        "drop trigger medicine_prescription_updated_at_trg on public.medicine_prescriptions;"
    )
    op.execute(
        "drop trigger medicine_prescription_deleted_at_trg on public.medicine_prescriptions;"
    )
    op.execute("drop table if exists public.medicine_prescriptions CASCADE;")
