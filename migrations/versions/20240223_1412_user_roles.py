"""user_roles

Revision ID: 76c177bcb84c
Revises: f95b98b5ee4c
Create Date: 2024-02-23 14:12:21.421146

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "76c177bcb84c"
down_revision: Union[str, None] = "f95b98b5ee4c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
    create table public.user_roles (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    constraint user_fk FOREIGN KEY (user_id)
    REFERENCES public.users(id) ON DELETE CASCADE,
    constraint role_fk FOREIGN KEY (role_id)
    REFERENCES public.roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
    );
    """
    )


def downgrade() -> None:
    op.execute("drop table public.user_roles;")
