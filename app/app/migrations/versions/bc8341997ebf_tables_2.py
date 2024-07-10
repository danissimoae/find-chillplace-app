"""Tables 2

Revision ID: bc8341997ebf
Revises: 39224837f523
Create Date: 2024-07-06 20:40:41.964073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc8341997ebf'
down_revision: Union[str, None] = '39224837f523'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
