"""Added Column stars to table hotels

Revision ID: fe7feb71358f
Revises: 6d87a40b0a49
Create Date: 2024-07-08 21:39:18.092169

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe7feb71358f'
down_revision: Union[str, None] = '6d87a40b0a49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hotels', sa.Column('stars', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hotels', 'stars')
    # ### end Alembic commands ###
