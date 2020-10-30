"""creating itemQuant table

Revision ID: b20bf9ae87ac
Revises: 20c25ad6e987
Create Date: 2020-02-11 01:39:34.595784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b20bf9ae87ac'
down_revision = '20c25ad6e987'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('item_quantity',
    sa.Column('item_quantity_id', sa.Integer(), nullable=False),
    sa.Column('quantity_needed', sa.Integer(), nullable=True),
    sa.Column('relief_item', sa.Integer(), nullable=True),
    sa.Column('disaster', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['disaster'], ['disaster_post.post_id'], ),
    sa.ForeignKeyConstraint(['relief_item'], ['relief_items.item_id'], ),
    sa.PrimaryKeyConstraint('item_quantity_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('item_quantity')
    # ### end Alembic commands ###
