"""clinical_assesments

Revision ID: da19609011a8
Revises: 006f92681953
Create Date: 2024-02-26 07:48:21.817494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da19609011a8'
down_revision: Union[str, None] = '006f92681953'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    create table clinical_assesments (
    id serial constraint clinical_assesment_pk primary key,
    
    patient_appointment_id integer not null constraint clinical_assesment_patient_appointment_fk
        references public.patient_appointments,
    patient_hospitalization_id integer not null constraint clinical_assesment_patient_hospitalization_fk
        references public.patient_hospitalizations,
    patient_id integer not null constraint clinical_assesment_patient_fk
        references public.patients,
    
    has_dyspnea boolean not null default false,
    distance_walking_6_minutes distance_walking_type not null default '<200',
    has_orthopnea boolean not null default false,
    has_night_dyspnea boolean not null default false,
    has_decreased_exercise_tolerance boolean not null default false,
    has_weakness boolean not null default false,
    has_increased_anknes boolean not null default false,
    has_night_cough boolean not null default false,
    has_weight_gain boolean not null default false,
    has_lose_weight boolean not null default false,
    has_depression boolean not null default false,
    has_increased_central_venous_pressure boolean not null default false,
    has_heartbeat boolean not null default false,
    has_hepatojugular_reflux boolean not null default false,
    has_third_ton boolean not null default false,
    has_displacement_of_the_apical boolean not null default false,
    has_peripheral_edema boolean not null default false,
    has_moist_rales boolean not null default false,
    has_heart_murmur boolean not null default false,
    has_tachycardia boolean not null default false,
    has_irregular_pulse boolean not null default false,
    has_tachypnea boolean not null default false,
    has_hepatomegaly boolean not null default false,
    has_ascites boolean not null default false,
    has_cachexia boolean not null default false,
    
    is_deleted boolean default false not null,
    
    created_at   timestamp with time zone default now() not null,
    created_by   integer not null,

    updated_at   timestamp with time zone,
    updated_by   integer,

    deleted_at   timestamp with time zone,
    deleted_by   integer
    );
    ''')

    op.execute('''
            create trigger clinical_assesment_updated_at_trg
            before update
            on public.clinical_assesments
            for each row
            execute procedure base.set_updated_at();
            ''')

    op.execute('''
                create trigger clinical_assesment_deleted_at_trg
                before update
                on public.clinical_assesments
                for each row
                execute procedure base.set_deleted_at();
                ''')



def downgrade() -> None:
    op.execute('drop trigger clinical_assesment_updated_at_trg on public.clinical_assesments;')
    op.execute('drop trigger clinical_assesment_deleted_at_trg on public.clinical_assesments;')
    op.execute('drop table public.clinical_assesments;')
