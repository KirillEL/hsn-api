"""initial_2

Revision ID: 2b8b57377f90
Revises: 9c1db95286ea
Create Date: 2024-02-12 13:16:18.768593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2b8b57377f90'
down_revision: Union[str, None] = '9c1db95286ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('analyses',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('count_index', sa.Integer(), nullable=False),
    sa.Column('patient_hospitalization_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['patient_hospitalization_id'], ['public.patient_hospitalizations.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('clinical_assesments',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('has_dyspnea', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('distance_walking_6_minutes', postgresql.ENUM('LOW', 'LOW_MEDIUM', 'MEDIUM', 'HIGH', name='distance_walking_type'), nullable=False),
    sa.Column('has_orthopnea', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_night_dyspnea', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_decreased_exercise_tolerance', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_weakness', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_increased_anknes', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_night_cough', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_weight_gain', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_lose_weight', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_depression', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_increased_central_venous_pressure', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_heartbeat', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.Column('has_hepatojugular_reflux', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_third_ton', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_displacement_of_the_apical', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_peripheral_edema', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_moist_rales', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_heart_murmur', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_tachycardia', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_irregular_pulse', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_tachypnea', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_hepatomegaly', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_ascites', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_cachexia', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('patient_appointment_id', sa.BigInteger(), nullable=False),
    sa.Column('patient_hospitalization_id', sa.BigInteger(), nullable=False),
    sa.Column('patient_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['patient_appointment_id'], ['public.patient_appointments.id'], ),
    sa.ForeignKeyConstraint(['patient_hospitalization_id'], ['public.patient_hospitalizations.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['public.patients.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('medicines_prescription',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('medicine_group_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('patient_appointment_id', sa.BigInteger(), nullable=False),
    sa.Column('patient_hospitalization_id', sa.BigInteger(), nullable=False),
    sa.Column('mnn', sa.String(length=200), nullable=True),
    sa.Column('dosa', sa.Integer(), nullable=False),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.Column('deleted_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['medicine_group_id'], ['public.medicines_group.id'], ),
    sa.ForeignKeyConstraint(['patient_appointment_id'], ['public.patient_appointments.id'], ),
    sa.ForeignKeyConstraint(['patient_hospitalization_id'], ['public.patient_hospitalizations.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('researchs',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('analyses_id', sa.BigInteger(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('patient_appointment_id', sa.BigInteger(), nullable=False),
    sa.Column('patient_hospitalization_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['analyses_id'], ['public.analyses.id'], ),
    sa.ForeignKeyConstraint(['patient_appointment_id'], ['public.patient_appointments.id'], ),
    sa.ForeignKeyConstraint(['patient_hospitalization_id'], ['public.patient_hospitalizations.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.drop_table('medicines_catalog')
    op.drop_constraint('cabinets_med_id_fkey', 'cabinets', type_='foreignkey')
    op.create_foreign_key(None, 'cabinets', 'med_organizations', ['med_id'], ['id'], source_schema='public', referent_schema='public')
    op.add_column('contragents', sa.Column('mis_number', sa.BigInteger(), nullable=False))
    op.add_column('contragents', sa.Column('date_birth', sa.Date(), nullable=False))
    op.add_column('contragents', sa.Column('relative_phone_number', sa.BigInteger(), nullable=False))
    op.add_column('contragents', sa.Column('parent', sa.Text(), nullable=True))
    op.add_column('contragents', sa.Column('date_dead', sa.Date(), nullable=True))
    op.add_column('diagnoses_catalog', sa.Column('note', sa.Text(), nullable=True))
    op.add_column('doctors', sa.Column('phone_number', sa.BigInteger(), nullable=False))
    op.create_unique_constraint(None, 'doctors', ['phone_number'], schema='public')
    op.drop_constraint('doctors_cabinet_id_fkey', 'doctors', type_='foreignkey')
    op.drop_constraint('doctors_user_id_fkey', 'doctors', type_='foreignkey')
    op.create_foreign_key(None, 'doctors', 'cabinets', ['cabinet_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'doctors', 'users', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.add_column('med_organizations', sa.Column('number', sa.Integer(), nullable=False))
    op.add_column('med_organizations', sa.Column('address', sa.Text(), nullable=False))
    op.create_unique_constraint(None, 'med_organizations', ['number'], schema='public')
    op.add_column('medicines_group', sa.Column('note', sa.Text(), nullable=True))
    op.add_column('medicines_group', sa.Column('patient_hospitalization_id', sa.BigInteger(), nullable=False))
    op.create_foreign_key(None, 'medicines_group', 'patient_hospitalizations', ['patient_hospitalization_id'], ['id'], source_schema='public', referent_schema='public')
    op.add_column('patient_appointments', sa.Column('date_next', sa.DateTime(), nullable=True))
    op.add_column('patient_appointments', sa.Column('fv_lg', sa.Integer(), nullable=False))
    op.add_column('patient_appointments', sa.Column('main_diagnose', sa.Text(), nullable=False))
    op.add_column('patient_appointments', sa.Column('sistol_ad', sa.Float(), nullable=False))
    op.add_column('patient_appointments', sa.Column('diastal_ad', sa.Float(), nullable=False))
    op.add_column('patient_appointments', sa.Column('hss', sa.Integer(), nullable=False))
    op.add_column('patient_appointments', sa.Column('mit', sa.Float(), nullable=True))
    op.add_column('patient_appointments', sa.Column('has_fatigue', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.add_column('patient_appointments', sa.Column('has_dyspnea', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.add_column('patient_appointments', sa.Column('has_swelling_legs', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.add_column('patient_appointments', sa.Column('has_weakness', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.add_column('patient_appointments', sa.Column('has_orthopnea', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.add_column('patient_appointments', sa.Column('has_heartbeat', sa.Boolean(), server_default=sa.text('true'), nullable=False))
    op.add_column('patient_appointments', sa.Column('note', sa.Text(), nullable=True))
    op.drop_constraint('patient_appointments_patient_id_fkey', 'patient_appointments', type_='foreignkey')
    op.drop_constraint('patient_appointments_doctor_id_fkey', 'patient_appointments', type_='foreignkey')
    op.drop_constraint('patient_appointments_cabinet_id_fkey', 'patient_appointments', type_='foreignkey')
    op.create_foreign_key(None, 'patient_appointments', 'doctors', ['doctor_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'patient_appointments', 'patients', ['patient_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'patient_appointments', 'cabinets', ['cabinet_id'], ['id'], source_schema='public', referent_schema='public')
    op.add_column('patient_hospitalizations', sa.Column('anamnes', sa.Text(), nullable=True))
    op.drop_constraint('patient_hospitalizations_patient_id_fkey', 'patient_hospitalizations', type_='foreignkey')
    op.create_foreign_key(None, 'patient_hospitalizations', 'patients', ['patient_id'], ['id'], source_schema='public', referent_schema='public')
    op.add_column('patients', sa.Column('height', sa.Integer(), nullable=False))
    op.add_column('patients', sa.Column('main_diagnose', sa.Text(), nullable=True))
    op.add_column('patients', sa.Column('age', sa.Integer(), nullable=True))
    op.add_column('patients', sa.Column('disability', postgresql.ENUM('NO_DISABILITY', 'FIRST_DISABILITY', 'SECOND_DISABILITY', 'THIRD_DISABILITY', name='disability', create_type=True), server_default=sa.text("'NO_DISABILITY'"), nullable=False))
    op.add_column('patients', sa.Column('date_setup_diagnose', sa.DateTime(), nullable=True))
    op.add_column('patients', sa.Column('school_hsn_date', sa.DateTime(), nullable=True))
    op.add_column('patients', sa.Column('have_hospitalization', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.add_column('patients', sa.Column('count_hospitalizations', sa.Integer(), nullable=False))
    op.add_column('patients', sa.Column('lgota_drugs', postgresql.ENUM('NO_LGOTA', 'LGOTA', 'LGOTA_MONEY', name='lgota_drugs', create_type=True), server_default=sa.text("'NO_LGOTA'"), nullable=False))
    op.add_column('patients', sa.Column('last_hospitalization_id', sa.BigInteger(), nullable=True))
    op.add_column('patients', sa.Column('note', sa.Text(), nullable=True))
    op.add_column('patients', sa.Column('has_chronic_heart', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.add_column('patients', sa.Column('classification_func_classes', postgresql.ENUM('FK1', 'FK2', 'FK3', 'FK4', name='classification_func_classes'), nullable=True))
    op.add_column('patients', sa.Column('has_stenocardia', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.add_column('patients', sa.Column('has_arteria_hypertension', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.add_column('patients', sa.Column('arteria_hypertension_age', sa.Integer(), nullable=True))
    op.drop_constraint('patients_cabinet_id_fkey', 'patients', type_='foreignkey')
    op.drop_constraint('patients_contragent_id_fkey', 'patients', type_='foreignkey')
    op.create_foreign_key(None, 'patients', 'cabinets', ['cabinet_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'patients', 'contragents', ['contragent_id'], ['id'], source_schema='public', referent_schema='public')
    op.add_column('supplied_diagnoses', sa.Column('diagnose_catalog_id', sa.BigInteger(), nullable=False))
    op.add_column('supplied_diagnoses', sa.Column('medicine_prescription_id', sa.BigInteger(), nullable=False))
    op.add_column('supplied_diagnoses', sa.Column('note', sa.Text(), nullable=True))
    op.drop_constraint('supplied_diagnoses_patient_appointment_id_fkey', 'supplied_diagnoses', type_='foreignkey')
    op.drop_constraint('supplied_diagnoses_diagnose_id_fkey', 'supplied_diagnoses', type_='foreignkey')
    op.create_foreign_key(None, 'supplied_diagnoses', 'patient_appointments', ['patient_appointment_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'supplied_diagnoses', 'diagnoses_catalog', ['diagnose_catalog_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'supplied_diagnoses', 'medicines_prescription', ['medicine_prescription_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_column('supplied_diagnoses', 'date_end')
    op.drop_column('supplied_diagnoses', 'date_start')
    op.drop_column('supplied_diagnoses', 'diagnose_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('supplied_diagnoses', sa.Column('diagnose_id', sa.BIGINT(), autoincrement=False, nullable=False))
    op.add_column('supplied_diagnoses', sa.Column('date_start', sa.DATE(), autoincrement=False, nullable=False))
    op.add_column('supplied_diagnoses', sa.Column('date_end', sa.DATE(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'supplied_diagnoses', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'supplied_diagnoses', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'supplied_diagnoses', schema='public', type_='foreignkey')
    op.create_foreign_key('supplied_diagnoses_diagnose_id_fkey', 'supplied_diagnoses', 'diagnoses_catalog', ['diagnose_id'], ['id'])
    op.create_foreign_key('supplied_diagnoses_patient_appointment_id_fkey', 'supplied_diagnoses', 'patient_appointments', ['patient_appointment_id'], ['id'])
    op.drop_column('supplied_diagnoses', 'note')
    op.drop_column('supplied_diagnoses', 'medicine_prescription_id')
    op.drop_column('supplied_diagnoses', 'diagnose_catalog_id')
    op.drop_constraint(None, 'patients', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'patients', schema='public', type_='foreignkey')
    op.create_foreign_key('patients_contragent_id_fkey', 'patients', 'contragents', ['contragent_id'], ['id'])
    op.create_foreign_key('patients_cabinet_id_fkey', 'patients', 'cabinets', ['cabinet_id'], ['id'])
    op.drop_column('patients', 'arteria_hypertension_age')
    op.drop_column('patients', 'has_arteria_hypertension')
    op.drop_column('patients', 'has_stenocardia')
    op.drop_column('patients', 'classification_func_classes')
    op.drop_column('patients', 'has_chronic_heart')
    op.drop_column('patients', 'note')
    op.drop_column('patients', 'last_hospitalization_id')
    op.drop_column('patients', 'lgota_drugs')
    op.drop_column('patients', 'count_hospitalizations')
    op.drop_column('patients', 'have_hospitalization')
    op.drop_column('patients', 'school_hsn_date')
    op.drop_column('patients', 'date_setup_diagnose')
    op.drop_column('patients', 'disability')
    op.drop_column('patients', 'age')
    op.drop_column('patients', 'main_diagnose')
    op.drop_column('patients', 'height')
    op.drop_constraint(None, 'patient_hospitalizations', schema='public', type_='foreignkey')
    op.create_foreign_key('patient_hospitalizations_patient_id_fkey', 'patient_hospitalizations', 'patients', ['patient_id'], ['id'])
    op.drop_column('patient_hospitalizations', 'anamnes')
    op.drop_constraint(None, 'patient_appointments', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'patient_appointments', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'patient_appointments', schema='public', type_='foreignkey')
    op.create_foreign_key('patient_appointments_cabinet_id_fkey', 'patient_appointments', 'cabinets', ['cabinet_id'], ['id'])
    op.create_foreign_key('patient_appointments_doctor_id_fkey', 'patient_appointments', 'doctors', ['doctor_id'], ['id'])
    op.create_foreign_key('patient_appointments_patient_id_fkey', 'patient_appointments', 'patients', ['patient_id'], ['id'])
    op.drop_column('patient_appointments', 'note')
    op.drop_column('patient_appointments', 'has_heartbeat')
    op.drop_column('patient_appointments', 'has_orthopnea')
    op.drop_column('patient_appointments', 'has_weakness')
    op.drop_column('patient_appointments', 'has_swelling_legs')
    op.drop_column('patient_appointments', 'has_dyspnea')
    op.drop_column('patient_appointments', 'has_fatigue')
    op.drop_column('patient_appointments', 'mit')
    op.drop_column('patient_appointments', 'hss')
    op.drop_column('patient_appointments', 'diastal_ad')
    op.drop_column('patient_appointments', 'sistol_ad')
    op.drop_column('patient_appointments', 'main_diagnose')
    op.drop_column('patient_appointments', 'fv_lg')
    op.drop_column('patient_appointments', 'date_next')
    op.drop_constraint(None, 'medicines_group', schema='public', type_='foreignkey')
    op.drop_column('medicines_group', 'patient_hospitalization_id')
    op.drop_column('medicines_group', 'note')
    op.drop_constraint(None, 'med_organizations', schema='public', type_='unique')
    op.drop_column('med_organizations', 'address')
    op.drop_column('med_organizations', 'number')
    op.drop_constraint(None, 'doctors', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'doctors', schema='public', type_='foreignkey')
    op.create_foreign_key('doctors_user_id_fkey', 'doctors', 'users', ['user_id'], ['id'])
    op.create_foreign_key('doctors_cabinet_id_fkey', 'doctors', 'cabinets', ['cabinet_id'], ['id'])
    op.drop_constraint(None, 'doctors', schema='public', type_='unique')
    op.drop_column('doctors', 'phone_number')
    op.drop_column('diagnoses_catalog', 'note')
    op.drop_column('contragents', 'date_dead')
    op.drop_column('contragents', 'parent')
    op.drop_column('contragents', 'relative_phone_number')
    op.drop_column('contragents', 'date_birth')
    op.drop_column('contragents', 'mis_number')
    op.drop_constraint(None, 'cabinets', schema='public', type_='foreignkey')
    op.create_foreign_key('cabinets_med_id_fkey', 'cabinets', 'med_organizations', ['med_id'], ['id'])
    op.create_table('medicines_catalog',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('code', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('group_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('is_deleted', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('deleted_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_by', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('updated_by', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('deleted_by', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['medicines_group.id'], name='medicines_catalog_group_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='medicines_catalog_pkey'),
    sa.UniqueConstraint('code', name='medicines_catalog_code_key')
    )
    op.drop_table('researchs', schema='public')
    op.drop_table('medicines_prescription', schema='public')
    op.drop_table('clinical_assesments', schema='public')
    op.drop_table('analyses', schema='public')
    # ### end Alembic commands ###
