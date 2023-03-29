"""upgraded5

Revision ID: fc3a19e684d6
Revises: 93d9356f1128
Create Date: 2023-03-23 19:48:50.353270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc3a19e684d6'
down_revision = '93d9356f1128'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orderitem', schema=None) as batch_op:
        batch_op.drop_column('order_id')
        batch_op.drop_column('vendor')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orderitem', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vendor', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('order_id', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###