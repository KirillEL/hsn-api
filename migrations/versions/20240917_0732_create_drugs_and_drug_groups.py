"""create drugs and drug_groups

Revision ID: b80b256ac835
Revises: 9cebace410bd
Create Date: 2024-09-17 07:32:49.032466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b80b256ac835'
down_revision: Union[str, None] = '9cebace410bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
            INSERT INTO public.drug_groups (id,name, is_deleted, created_by) VALUES
            (1,'b-АБ', false, 1),
            (2,'Глифозины', false, 1),
            (3,'Статины', false, 1),
            (4,'АМКР', false, 1),
            (5,'АРНИ', false, 1),
            (6,'АПФ', false, 1),
            (7,'САРТАНЫ', false, 1),
            (8,'АСК', false, 1),
            (9,'ПОАК или АВК', false, 1),
            (10,'БМКК', false, 1),
            (11,'Нитраты', false, 1),
            (12,'Диуретики', false, 1),
            (13,'Антиаритмики', false, 1),
            (14,'Ивабрадин', false, 1),
            (15,'Дизагреганты', false, 1),
            (16,'Сердечные гликозиды', false, 1);
        """)

    # Получаем ID каждой группы для дальнейшего использования
    groups = {
        'b-АБ': 1,
        'Глифозины': 2,
        'Статины': 3,
        'АМКР': 4,
        'АРНИ': 5,
        'АПФ': 6,
        'САРТАНЫ': 7,
        'АСК': 8,
        'ПОАК или АВК': 9,
        'БМКК': 10,
        'Нитраты': 11,
        'Диуретики': 12,
        'Антиаритмики': 13,
        'Ивабрадин': 14,
        'Дизагреганты': 15,
        'Сердечные гликозиды': 16
    }

    # Далее создаем препараты, связывая их с соответствующими группами
    op.execute(f"""
            INSERT INTO public.drugs (name, drug_group_id, is_deleted) VALUES
            ('Бисопролол', {groups['b-АБ']}, false),
            ('Метопролол', {groups['b-АБ']}, false),
            ('Другое', {groups['b-АБ']}, false),
            ('Дапаглифлозин', {groups['Глифозины']}, false),
            ('Эмпаглифлозин', {groups['Глифозины']}, false),
            ('Другое', {groups['Глифозины']}, false),
            ('Аторвастатин', {groups['Статины']}, false),
            ('Симвастатин', {groups['Статины']}, false),
            ('Другое', {groups['Статины']}, false),
            ('Изосорбидмононитрат', {groups['АМКР']}, false),
            ('Спиронолактон', {groups['АМКР']}, false),
            ('Другое', {groups['АМКР']}, false),
            ('Валсартан + Сакубитрил', {groups['АРНИ']}, false),
            ('Юперио', {groups['АРНИ']}, false),
            ('Другое', {groups['АРНИ']}, false),
            ('Периндоприл', {groups['АПФ']}, false),
            ('Эналаприл', {groups['АПФ']}, false),
            ('Другое', {groups['АПФ']}, false),
            ('Лозартан', {groups['САРТАНЫ']}, false),
            ('Другое', {groups['САРТАНЫ']}, false),
            ('Ацетил-салициловая кислота', {groups['АСК']}, false),
            ('Другое', {groups['АСК']}, false),
            ('Апиксабан', {groups['ПОАК или АВК']}, false),
            ('Варфарин', {groups['ПОАК или АВК']}, false),
            ('Дабигатранаэтексилат', {groups['ПОАК или АВК']}, false),
            ('Ривароксабан', {groups['ПОАК или АВК']}, false),
            ('Другое', {groups['ПОАК или АВК']}, false),
            ('Амлодипин', {groups['БМКК']}, false),
            ('Другое', {groups['БМКК']}, false),
            ('Другое', {groups['Нитраты']}, false),
            ('Фуросемид', {groups['Диуретики']}, false),
            ('Индапамид', {groups['Диуретики']}, false),
            ('Гидрохлоротиазид', {groups['Диуретики']}, false),
            ('Ацетазоламид (диакарб)', {groups['Диуретики']}, false),
            ('Другое', {groups['Диуретики']}, false),
            ('Амиодарон', {groups['Антиаритмики']}, false),
            ('Лаппоканитина гидробрамид', {groups['Антиаритмики']}, false),
            ('Пропафенон', {groups['Антиаритмики']}, false),
            ('Соталол', {groups['Антиаритмики']}, false),
            ('Другое', {groups['Антиаритмики']}, false),
            ('Другое', {groups['Ивабрадин']}, false),
            ('Тикагрелол', {groups['Дизагреганты']}, false),
            ('Клопидогрел', {groups['Дизагреганты']}, false),
            ('Другое', {groups['Дизагреганты']}, false),
            ('Дигоксин', {groups['Сердечные гликозиды']}, false),
            ('Другое', {groups['Сердечные гликозиды']}, false);
        """)


def downgrade() -> None:
    op.execute(
        """
        TRUNCATE public.drugs CASCADE;
        """
    )

    op.execute(
        """
        TRUNCATE public.drug_groups CASCADE;
        """
    )
    # op.execute("""
    #         DELETE FROM public.drugs WHERE name IN (
    #             'Бисопролол', 'Метопролол', 'Другое', 'Дапаглифлозин', 'Эмпаглифлозин', 'Другое',
    #             'Аторвастатин', 'Симвастатин', 'Другое', 'Изосорбидмононитрат', 'Спиронолактон', 'Другое',
    #             'Валсартан + Сакубитрил', 'Юперио', 'Другое', 'Периндоприл', 'Эналаприл', 'Другое',
    #             'Лозартан', 'Другое', 'Ацетил-салициловая кислота', 'Другое', 'Апиксабан', 'Варфарин',
    #             'Дабигатранаэтексилат', 'Ривароксабан', 'Другое', 'Амлодипин', 'Другое', 'Другое',
    #             'Фуросемид', 'Индапамид', 'Гидрохлоротиазид', 'Ацетазоламид (диакарб)', 'Другое',
    #             'Амиодарон', 'Лаппоканитина гидробрамид', 'Пропафенон', 'Соталол', 'Другое', 'Другое',
    #             'Тикагрелол', 'Клопидогрел', 'Другое', 'Дигоксин', 'Другое'
    #         );
    #     """)
    # op.execute("""
    #         DELETE FROM public.drug_groups WHERE name IN (
    #             'b-АБ', 'Глифозины', 'Статины', 'АМКР', 'АРНИ', 'АПФ', 'САРТАНЫ', 'АСК',
    #             'ПОАК или АВК', 'БМКК', 'Нитраты', 'Диуретики', 'Антиаритмики', 'Ивабрадин',
    #             'Дизагреганты', 'Сердечные гликозиды'
    #         );
    #     """)
