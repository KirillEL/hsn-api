"""patient_appointments

Revision ID: 94cef94d62e8
Revises: 133bc396df29
Create Date: 2024-02-26 07:40:29.945237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94cef94d62e8'
down_revision: Union[str, None] = '133bc396df29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table public.patient_appointments (
    id serial constraint patient_appointments_pk primary key,
    patient_id integer not null constraint patient_appointment_patient_fk
        references public.patients ON DELETE CASCADE,
    doctor_id integer not null constraint patient_appointment_doctor_fk
        references public.doctors ON DELETE CASCADE,
    cabinet_id integer not null constraint patient_appointment_cabinet_fk
        references public.cabinets ON DELETE CASCADE,
    
    date timestamp with time zone not null,
    date_next timestamp with time zone,
    imt float not null,
    weight float not null,
    height float not null,  
    disability disability_type not null default 'no',
    school_hsn_date timestamp with time zone,
    classification_func_classes classification_func_classes_type not null default 'fk1',
    classification_adjacent_release classification_adjacent_release_type default null,
    classification_nc_stage classification_nc_stage_type default null,
    has_stenocardia_napryzenya boolean not null default false,
    has_myocardial_infarction boolean not null default false,
    has_arteria_hypertension boolean not null default false,
    arteria_hypertension_age integer,
    fv_lg integer not null,
    main_diagnose text not null,
    sistol_ad float not null,
    diastal_ad float not null,
    hss integer not null,
    mit float,
    
    has_fatigue boolean not null default false,
    has_dyspnea boolean not null default false,
    has_swelling_legs boolean not null default false,
    has_weakness boolean not null default false,
    has_orthopnea boolean not null default false,
    has_heartbeat boolean not null default true,
    note_complaints text,
    note_clinical text,
    note_ekg text,
    date_ekg timestamp without time zone,
    date_echo_ekg timestamp without time zone,
    fraction_out float not null,
    sdla float not null,
    
    nt_pro_bnp float not null,
    date_nt_pro_bnp timestamp without time zone,
    microalbumuria float not null,
    date_microalbumuria timestamp without time zone,
    

    is_deleted boolean not null default false,
    
    created_at   timestamp with time zone default now() not null,
    created_by   integer not null,

    updated_at   timestamp with time zone,
    updated_by   integer,

    deleted_at   timestamp with time zone,
    deleted_by   integer
    );
    ''')

    op.execute('''
            create trigger patient_appointment_updated_at_trg
            before update
            on public.patient_appointments
            for each row
            execute procedure base.set_updated_at();
            ''')

    op.execute('''
                create trigger patient_appointment_deleted_at_trg
                before update
                on public.patient_appointments
                for each row
                execute procedure base.set_deleted_at();
                ''')


def downgrade() -> None:
    op.execute('drop trigger patient_appointment_updated_at_trg on public.patient_appointments;')
    op.execute('drop trigger patient_appointment_deleted_at_trg on public.patient_appointments;')
    op.execute('drop table patient_appointments;')


