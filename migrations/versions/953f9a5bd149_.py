"""empty message

Revision ID: 953f9a5bd149
Revises: bca1943c271f
Create Date: 2024-05-06 15:12:36.227980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '953f9a5bd149'
down_revision: Union[str, None] = 'bca1943c271f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Basket',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fk_User', sa.Integer(), nullable=False),
    sa.Column('Price', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['fk_User'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ShoppingCartList',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fk_Dish', sa.Integer(), nullable=False),
    sa.Column('Amount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['fk_Dish'], ['Dish.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ShoppingCartList')
    op.drop_table('Basket')
    # ### end Alembic commands ###