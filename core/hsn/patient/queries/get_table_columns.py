from shared.db.db_session import db_session, SessionContext
from shared.db.models.patient_columns import PatientTableColumnsDBModel
from loguru import logger
from sqlalchemy import select

default_payload = [
    {
        "title": "ID",
        "dataIndex": "id",
        "key": "1",
        "dataType": "string",
        "canBeNull": False,
        "sorter": True,
        "width": 75,
    },
    {
        "title": "ФИО",
        "dataIndex": "full_name",
        "key": "2",
        "dataType": "string",
        "canBeNull": False,
        "filter": "searchTableFilter",
        "sorter": True,
        "width": 200,
    },
    {
        "title": "Возраст",
        "dataIndex": "age",
        "key": "3",
        "dataType": "string",
        "canBeNull": False,
        "filter": "intervalTableFilter",
        "sorter": True,
        "width": 50,
    },
    {
        "title": "Примечание",
        "dataIndex": "patient_note",
        "key": "4",
        "dataType": "string",
        "canBeNull": True,
        "sorter": False,
        "width": 150,
    },
]


@SessionContext()
async def hsn_query_patient_columns(user_id: int):
    query = select(PatientTableColumnsDBModel.table_columns).where(
        PatientTableColumnsDBModel.user_id == user_id
    )
    cursor = await db_session.execute(query)
    patient_table_columns = cursor.scalars().first()
    if not patient_table_columns:
        return default_payload

    patient_data_indices = {col["dataIndex"] for col in patient_table_columns}

    for column in default_payload:
        data_index = column["dataIndex"]
        for patient_col in patient_table_columns:
            if data_index == patient_col["dataIndex"]:
                if patient_col.get("hidden", False):
                    column["hidden"] = True
                elif "hidden" in column:
                    del column["hidden"]

    filtered_payload = [
        column
        for column in default_payload
        if column["dataIndex"] in patient_data_indices
    ]

    title_to_key_map = {
        col["dataIndex"]: i + 1 for i, col in enumerate(patient_table_columns)
    }

    for column in filtered_payload:
        title = column["dataIndex"]
        if title in title_to_key_map:
            column["key"] = str(title_to_key_map[title])

    sorted_payload = sorted(filtered_payload, key=lambda x: int(x["key"]))
    return sorted_payload
