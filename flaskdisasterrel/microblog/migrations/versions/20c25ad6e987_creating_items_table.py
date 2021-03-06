"""creating items table

Revision ID: 20c25ad6e987
Revises: 70d31eeef994
Create Date: 2020-02-11 01:39:13.752608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20c25ad6e987'
down_revision = '70d31eeef994'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('relief_items',
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('item_id')
    )
    op.create_index(op.f('ix_relief_items_item_name'), 'relief_items', ['item_name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_relief_items_item_name'), table_name='relief_items')
    op.drop_table('relief_items')
    # ### end Alembic commands ###
