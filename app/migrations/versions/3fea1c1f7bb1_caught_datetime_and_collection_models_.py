"""Caught datetime and collection models configured

Revision ID: 3fea1c1f7bb1
Revises: 7a5abe667204
Create Date: 2025-06-14 11:54:19.518034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fea1c1f7bb1'
down_revision = '7a5abe667204'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('caught_date', schema=None) as batch_op:
        batch_op.add_column(sa.Column('startdate', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('enddate', sa.Date(), nullable=True))
        batch_op.drop_column('date_range')

    with op.batch_alter_table('caught_time', schema=None) as batch_op:
        batch_op.add_column(sa.Column('starttime', sa.Time(), nullable=True))
        batch_op.add_column(sa.Column('endtime', sa.Time(), nullable=True))
        batch_op.drop_column('time_range')

    with op.batch_alter_table('collection_completion', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('collection_completion', schema=None) as batch_op:
        batch_op.drop_column('name')

    with op.batch_alter_table('caught_time', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time_range', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('endtime')
        batch_op.drop_column('starttime')

    with op.batch_alter_table('caught_date', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_range', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('enddate')
        batch_op.drop_column('startdate')

    # ### end Alembic commands ###
