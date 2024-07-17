"""type parameter migrations

Revision ID: d279531e471c
Revises: 58a5206d5805
Create Date: 2024-07-16 22:42:48.314810

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.modules.parameter.entities.models import TypeParameter


# revision identifiers, used by Alembic.
revision: str = 'd279531e471c'
down_revision: Union[str, None] = '58a5206d5805'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        # Seed initial data
    initial_data = [
        {"name": "number"},
        {"name": "json"},
        {"name": "boolean"},
        {"name": "string"},
        {"name": "array"},
    ]

    # Insert initial data
    for entry in initial_data:
        op.get_bind().execute(TypeParameter.__table__.insert().values(**entry))

    pass



def downgrade() -> None:
    pass
