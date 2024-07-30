"""roles

Revision ID: c1ba7eec30e7
Revises: 9e845d5c5eab
Create Date: 2024-02-23 13:47:24.085632

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c1ba7eec30e7"
down_revision: Union[str, None] = "9e845d5c5eab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
    create table public.roles (
    id serial constraint roles_pk primary key,
    name varchar(50) UNIQUE NOT NULL
    );
    """
    )


def downgrade() -> None:
    op.execute("drop table public.roles;")
