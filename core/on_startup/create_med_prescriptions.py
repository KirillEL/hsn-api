from loguru import logger
from sqlalchemy import insert, select, func
from shared.db.models.medicines_prescription import MedicinesPrescriptionDBModel
from shared.db.db_session import db_session, SessionContext

med_groups = {
    "BAB": "b-АБ",
    "GLYPHOZYN": "Глифозины",
    "STATIN": "Статины",
    "AMKR": "АМКР",
    "ARNI": "АРНИ",
    "APF": "АПФ",
    "SARTAN": "САРТАНЫ",
    "ASK": "АСК",
    "POAK_AVK": "ПОАК или АВК",
    "BMKK": "БМКК",
    "NITRAT": "Нитраты",
    "DIURETIC": "Диуретики",
    "ANTIARITMIC": "Антиаритмики",
    "IVABRADIN": "Ивабрадин",
    "DIZAGREGANT": "Дизагреганты",
    "GLYKOLIS": "Сердечные гликозиды",
    "GYPOTENZ": "Гипотензивные",
    "ANOTHER": "Другое"
}

payloads = {
    "b-АБ": ["Бисопролол", "Метопролол", "Другое"],
    "Глифозины": ["Дапаглифлозин", "Эмпаглифлозин", "Другое"],
    "Статины": ["Аторвастатин", "Симвастатин", "Другое"],
    "АМКР": ["Изосорбидмононитрат", "Спиронолактон", "Другое"],
    "АРНИ": ["Валсартан + Сакубитрил", "Юперио", "Другое"],
    "АПФ": ["Периндоприл", "Эналаприл", "Другое"],
    "САРТАНЫ": ["Лозартан", "Другое"],
    "АСК": ["Ацетил-салициловая кислота", "Другое"],
    "ПОАК или АВК": ["Апиксабан", "Варфарин", "Дабигатранаэтексилат", "Ривароксабан", "Другое"],
    "БМКК": ["Амлодипин", "Другое"],
    "Нитраты": ["Другое"],
    "Диуретики": ["Фуросемид", "Индапамид", "Гидрохлоротиазид", "Ацетазоламид (диакарб)", "Другое"],
    "Антиаритмики": ["Амиодарон", "Лаппоканитина гидробрамид", "Пропафенон", "Соталол", "Другое"],
    "Ивабрадин": ["Другое"],
    "Дизагреганты": ["Тикагрелол", "Клопидогрел", "Другое"],
    "Сердечные гликозиды": ["Дигоксин", "Другое"],
    "Гипотензивные центр. действия": ["Моксонидин", "Другое"]
}


@SessionContext()
async def create_med_prescriptions():
    query = (
        select(func.count()).select_from(MedicinesPrescriptionDBModel).where(MedicinesPrescriptionDBModel.is_deleted.is_(False))
    )
    cursor = await db_session.execute(query)
    count = cursor.scalar()
    if count != 0:
        logger.info("Препараты созданы уже!")
        return
    logger.debug(f'count {count}')
    for group, names in payloads.items():
        for name in names:
            prescription = MedicinesPrescriptionDBModel(
                medicine_group=group,
                name=name
            )
            db_session.add(prescription)

    await db_session.commit()
    logger.info("Препараты созданы...")