"""update_1

Revision ID: e26d99bb1d4e
Revises: 35a2ddbc3653
Create Date: 2024-02-13 06:41:27.181830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e26d99bb1d4e'
down_revision: Union[str, None] = '35a2ddbc3653'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('analyses_patient_hospitalization_id_fkey', 'analyses', type_='foreignkey')
    op.create_foreign_key(None, 'analyses', 'patient_hospitalizations', ['patient_hospitalization_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('cabinets_med_id_fkey', 'cabinets', type_='foreignkey')
    op.create_foreign_key(None, 'cabinets', 'med_organizations', ['med_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('clinical_assesments_patient_appointment_id_fkey', 'clinical_assesments', type_='foreignkey')
    op.drop_constraint('clinical_assesments_patient_id_fkey', 'clinical_assesments', type_='foreignkey')
    op.drop_constraint('clinical_assesments_patient_hospitalization_id_fkey', 'clinical_assesments', type_='foreignkey')
    op.create_foreign_key(None, 'clinical_assesments', 'patient_hospitalizations', ['patient_hospitalization_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'clinical_assesments', 'patients', ['patient_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'clinical_assesments', 'patient_appointments', ['patient_appointment_id'], ['id'], source_schema='public', referent_schema='public')
    op.alter_column('doctors', 'cabinet_id',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.drop_constraint('doctors_user_id_fkey', 'doctors', type_='foreignkey')
    op.drop_constraint('doctors_cabinet_id_fkey', 'doctors', type_='foreignkey')
    op.create_foreign_key(None, 'doctors', 'cabinets', ['cabinet_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'doctors', 'users', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('medicines_prescription_patient_appointment_id_fkey', 'medicines_prescription', type_='foreignkey')
    op.drop_constraint('medicines_prescription_patient_hospitalization_id_fkey', 'medicines_prescription', type_='foreignkey')
    op.drop_constraint('medicines_prescription_medicine_group_id_fkey', 'medicines_prescription', type_='foreignkey')
    op.create_foreign_key(None, 'medicines_prescription', 'medicines_group', ['medicine_group_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'medicines_prescription', 'patient_appointments', ['patient_appointment_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'medicines_prescription', 'patient_hospitalizations', ['patient_hospitalization_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('patient_appointments_doctor_id_fkey', 'patient_appointments', type_='foreignkey')
    op.drop_constraint('patient_appointments_cabinet_id_fkey', 'patient_appointments', type_='foreignkey')
    op.drop_constraint('patient_appointments_patient_id_fkey', 'patient_appointments', type_='foreignkey')
    op.create_foreign_key(None, 'patient_appointments', 'patients', ['patient_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'patient_appointments', 'cabinets', ['cabinet_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'patient_appointments', 'doctors', ['doctor_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('patient_hospitalizations_patient_id_fkey', 'patient_hospitalizations', type_='foreignkey')
    op.create_foreign_key(None, 'patient_hospitalizations', 'patients', ['patient_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('patients_contragent_id_fkey', 'patients', type_='foreignkey')
    op.drop_constraint('patients_cabinet_id_fkey', 'patients', type_='foreignkey')
    op.create_foreign_key(None, 'patients', 'contragents', ['contragent_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'patients', 'cabinets', ['cabinet_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('researchs_analyses_id_fkey', 'researchs', type_='foreignkey')
    op.drop_constraint('researchs_patient_appointment_id_fkey', 'researchs', type_='foreignkey')
    op.drop_constraint('researchs_patient_hospitalization_id_fkey', 'researchs', type_='foreignkey')
    op.create_foreign_key(None, 'researchs', 'patient_appointments', ['patient_appointment_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'researchs', 'patient_hospitalizations', ['patient_hospitalization_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'researchs', 'analyses', ['analyses_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('supplied_diagnoses_diagnose_catalog_id_fkey', 'supplied_diagnoses', type_='foreignkey')
    op.drop_constraint('supplied_diagnoses_patient_appointment_id_fkey', 'supplied_diagnoses', type_='foreignkey')
    op.drop_constraint('supplied_diagnoses_medicine_prescription_id_fkey', 'supplied_diagnoses', type_='foreignkey')
    op.create_foreign_key(None, 'supplied_diagnoses', 'medicines_prescription', ['medicine_prescription_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'supplied_diagnoses', 'diagnoses_catalog', ['diagnose_catalog_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'supplied_diagnoses', 'patient_appointments', ['patient_appointment_id'], ['id'], source_schema='public', referent_schema='public')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'supplied_diagnoses', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'supplied_diagnoses', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'supplied_diagnoses', schema='public', type_='foreignkey')
    op.create_foreign_key('supplied_diagnoses_medicine_prescription_id_fkey', 'supplied_diagnoses', 'medicines_prescription', ['medicine_prescription_id'], ['id'])
    op.create_foreign_key('supplied_diagnoses_patient_appointment_id_fkey', 'supplied_diagnoses', 'patient_appointments', ['patient_appointment_id'], ['id'])
    op.create_foreign_key('supplied_diagnoses_diagnose_catalog_id_fkey', 'supplied_diagnoses', 'diagnoses_catalog', ['diagnose_catalog_id'], ['id'])
    op.drop_constraint(None, 'researchs', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'researchs', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'researchs', schema='public', type_='foreignkey')
    op.create_foreign_key('researchs_patient_hospitalization_id_fkey', 'researchs', 'patient_hospitalizations', ['patient_hospitalization_id'], ['id'])
    op.create_foreign_key('researchs_patient_appointment_id_fkey', 'researchs', 'patient_appointments', ['patient_appointment_id'], ['id'])
    op.create_foreign_key('researchs_analyses_id_fkey', 'researchs', 'analyses', ['analyses_id'], ['id'])
    op.drop_constraint(None, 'patients', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'patients', schema='public', type_='foreignkey')
    op.create_foreign_key('patients_cabinet_id_fkey', 'patients', 'cabinets', ['cabinet_id'], ['id'])
    op.create_foreign_key('patients_contragent_id_fkey', 'patients', 'contragents', ['contragent_id'], ['id'])
    op.drop_constraint(None, 'patient_hospitalizations', schema='public', type_='foreignkey')
    op.create_foreign_key('patient_hospitalizations_patient_id_fkey', 'patient_hospitalizations', 'patients', ['patient_id'], ['id'])
    op.drop_constraint(None, 'patient_appointments', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'patient_appointments', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'patient_appointments', schema='public', type_='foreignkey')
    op.create_foreign_key('patient_appointments_patient_id_fkey', 'patient_appointments', 'patients', ['patient_id'], ['id'])
    op.create_foreign_key('patient_appointments_cabinet_id_fkey', 'patient_appointments', 'cabinets', ['cabinet_id'], ['id'])
    op.create_foreign_key('patient_appointments_doctor_id_fkey', 'patient_appointments', 'doctors', ['doctor_id'], ['id'])
    op.drop_constraint(None, 'medicines_prescription', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'medicines_prescription', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'medicines_prescription', schema='public', type_='foreignkey')
    op.create_foreign_key('medicines_prescription_medicine_group_id_fkey', 'medicines_prescription', 'medicines_group', ['medicine_group_id'], ['id'])
    op.create_foreign_key('medicines_prescription_patient_hospitalization_id_fkey', 'medicines_prescription', 'patient_hospitalizations', ['patient_hospitalization_id'], ['id'])
    op.create_foreign_key('medicines_prescription_patient_appointment_id_fkey', 'medicines_prescription', 'patient_appointments', ['patient_appointment_id'], ['id'])
    op.drop_constraint(None, 'doctors', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'doctors', schema='public', type_='foreignkey')
    op.create_foreign_key('doctors_cabinet_id_fkey', 'doctors', 'cabinets', ['cabinet_id'], ['id'])
    op.create_foreign_key('doctors_user_id_fkey', 'doctors', 'users', ['user_id'], ['id'])
    op.alter_column('doctors', 'cabinet_id',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.drop_constraint(None, 'clinical_assesments', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'clinical_assesments', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'clinical_assesments', schema='public', type_='foreignkey')
    op.create_foreign_key('clinical_assesments_patient_hospitalization_id_fkey', 'clinical_assesments', 'patient_hospitalizations', ['patient_hospitalization_id'], ['id'])
    op.create_foreign_key('clinical_assesments_patient_id_fkey', 'clinical_assesments', 'patients', ['patient_id'], ['id'])
    op.create_foreign_key('clinical_assesments_patient_appointment_id_fkey', 'clinical_assesments', 'patient_appointments', ['patient_appointment_id'], ['id'])
    op.drop_constraint(None, 'cabinets', schema='public', type_='foreignkey')
    op.create_foreign_key('cabinets_med_id_fkey', 'cabinets', 'med_organizations', ['med_id'], ['id'])
    op.drop_constraint(None, 'analyses', schema='public', type_='foreignkey')
    op.create_foreign_key('analyses_patient_hospitalization_id_fkey', 'analyses', 'patient_hospitalizations', ['patient_hospitalization_id'], ['id'])
    # ### end Alembic commands ###