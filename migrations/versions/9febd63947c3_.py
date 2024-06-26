"""empty message

Revision ID: 9febd63947c3
Revises: 3b81a5bce488
Create Date: 2024-05-04 15:57:58.955621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9febd63947c3'
down_revision: Union[str, None] = '3b81a5bce488'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Users', 'Salt')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('Salt', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
