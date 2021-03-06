"""disaster items and quantity table created

Revision ID: e513af3c7b03
Revises: 2d563e8487af
Create Date: 2020-02-11 01:22:10.156955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e513af3c7b03'
down_revision = '2d563e8487af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('relief_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_relief_items_item_name'), 'relief_items', ['item_name'], unique=True)
    op.add_column(u'disaster_post', sa.Column('recipient_address', sa.VARCHAR(length=150), nullable=True))
    op.add_column(u'user', sa.Column('user_address', sa.VARCHAR(length=150), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'user', 'user_address')
    op.drop_column(u'disaster_post', 'recipient_address')
    op.drop_index(op.f('ix_relief_items_item_name'), table_name='relief_items')
    op.drop_table('relief_items')
    # ### end Alembic commands ###
