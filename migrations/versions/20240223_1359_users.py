"""users

Revision ID: f95b98b5ee4c
Revises: c9c032fedc0f
Create Date: 2024-02-23 13:59:39.966609

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f95b98b5ee4c"
down_revision: Union[str, None] = "c9c032fedc0f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
    create table public.users (
    id serial constraint users_pk primary key,
    login varchar(255) UNIQUE NOT NULL,
    password text NOT NULL,
    is_active boolean DEFAULT true,
    is_deleted boolean DEFAULT false
    );
    """
    )


def downgrade() -> None:
    op.execute("drop table public.users;")
