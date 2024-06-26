"""empty message

Revision ID: 3b81a5bce488
Revises: ad2db651b3ed
Create Date: 2024-05-04 15:49:51.085755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b81a5bce488'
down_revision: Union[str, None] = 'ad2db651b3ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('Salt', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Users', 'Salt')
    # ### end Alembic commands ###
