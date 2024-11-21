"""analises

Revision ID: 400249a20df2
Revises: 94cef94d62e8
Create Date: 2024-02-26 07:44:27.455128

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "400249a20df2"
down_revision: Union[str, None] = "94cef94d62e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
    create table public.analises (
    id serial constraint analises_pk primary key,
    name varchar(255) not null,
    count_index integer not null,
    
    is_deleted boolean not null default false,
    
    created_at   timestamp with time zone default now() not null,
    created_by   integer not null,

    updated_at   timestamp with time zone,
    updated_by   integer,

    deleted_at   timestamp with time zone,
    deleted_by   integer
    );
    """
    )

    op.execute(
        """
            create trigger analises_updated_at_trg
            before update
            on public.analises
            for each row
            execute procedure base.set_updated_at();
            """
    )

    op.execute(
        """
                create trigger analises_deleted_at_trg
                before update
                on public.analises
                for each row
                execute procedure base.set_deleted_at();
                """
    )


def downgrade() -> None:
    op.execute("drop trigger analises_updated_at_trg on public.analises;")
    op.execute("drop trigger analises_deleted_at_trg on public.analises;")
    op.execute("drop table public.analises;")
