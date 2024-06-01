"""empty message

Revision ID: 94aa848a2e7b
Revises: fcf7b456e28e
Create Date: 2024-05-14 13:42:18.122407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '94aa848a2e7b'
down_revision: Union[str, None] = 'fcf7b456e28e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Changes_Status_Order_fk_Order_fkey', 'Changes_Status_Order', type_='foreignkey')
    op.drop_constraint('Changes_Status_Order_fk_Status_fkey', 'Changes_Status_Order', type_='foreignkey')
    op.drop_constraint('Changes_Status_Bron_fk_Order_fkey', 'Changes_Status_Bron', type_='foreignkey')
    op.drop_constraint('Changes_Status_Bron_fk_Status_fkey', 'Changes_Status_Bron', type_='foreignkey')
    op.create_table('BronStatus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fk_Order', sa.Integer(), nullable=False),
    sa.Column('Status', sa.String(length=255), nullable=False),
    sa.Column('Time', sa.Time(), nullable=False),
    sa.Column('Date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['fk_Order'], ['Bron.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('OrderStatus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fk_Order', sa.Integer(), nullable=False),
    sa.Column('Status', sa.String(length=255), nullable=False),
    sa.Column('Time', sa.Time(), nullable=False),
    sa.Column('Date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['fk_Order'], ['Order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('Bron_Status')
    op.drop_table('Changes_Status_Order')
    op.drop_table('Changes_Status_Bron')
    op.drop_table('Order_Status')
    op.drop_table('ShoppingCartList')
    op.drop_table('ShoppingCart')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ShoppingCart',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"ShoppingCart_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('fk_User', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['fk_User'], ['Users.id'], name='ShoppingCart_fk_User_fkey'),
    sa.PrimaryKeyConstraint('id', name='ShoppingCart_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('ShoppingCartList',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"ShoppingCartList_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('fk_Dish', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Amount', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('fk_ShoppingCart', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['fk_Dish'], ['Dish.id'], name='ShoppingCartList_fk_Dish_fkey'),
    sa.ForeignKeyConstraint(['fk_ShoppingCart'], ['ShoppingCart.id'], name='ShoppingCartList_fk_ShoppingCart_fkey'),
    sa.PrimaryKeyConstraint('id', name='ShoppingCartList_pkey')
    )
    op.create_table('Order_Status',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Order_Status_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('Name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='Order_Status_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('Changes_Status_Bron',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Changes_Status_Bron_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('fk_Order', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('fk_Status', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Time', postgresql.TIME(), autoincrement=False, nullable=False),
    sa.Column('Date', sa.DATE(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['fk_Order'], ['Bron.id'], name='Changes_Status_Bron_fk_Order_fkey'),
    sa.ForeignKeyConstraint(['fk_Status'], ['Bron_Status.id'], name='Changes_Status_Bron_fk_Status_fkey'),
    sa.PrimaryKeyConstraint('id', name='Changes_Status_Bron_pkey')
    )
    op.create_table('Changes_Status_Order',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Changes_Status_Order_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('fk_Order', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('fk_Status', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Time', postgresql.TIME(), autoincrement=False, nullable=False),
    sa.Column('Date', sa.DATE(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['fk_Order'], ['Order.id'], name='Changes_Status_Order_fk_Order_fkey'),
    sa.ForeignKeyConstraint(['fk_Status'], ['Order_Status.id'], name='Changes_Status_Order_fk_Status_fkey'),
    sa.PrimaryKeyConstraint('id', name='Changes_Status_Order_pkey')
    )
    op.create_table('Bron_Status',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Bron_Status_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('Name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='Bron_Status_pkey')
    )
    op.drop_table('OrderStatus')
    op.drop_table('BronStatus')
    # ### end Alembic commands ###
