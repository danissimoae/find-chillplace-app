"""Tables

Revision ID: 39224837f523
Revises: ede33ee1d0bf
Create Date: 2024-07-06 17:59:31.589088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39224837f523'
down_revision: Union[str, None] = 'ede33ee1d0bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
