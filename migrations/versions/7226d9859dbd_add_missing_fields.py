"""add missing fields

Revision ID: 7226d9859dbd
Revises: 4fc4d647ffad
Create Date: 2025-06-09 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7226d9859dbd'
down_revision = '4fc4d647ffad'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('decoration_category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))

    with op.batch_alter_table('club', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=False))

    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))

    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('amount', sa.Float(), nullable=False))
        batch_op.add_column(sa.Column('status', sa.String(), nullable=False))

    with op.batch_alter_table('outfit_template', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('style', sa.String(), nullable=True))


def downgrade():
    with op.batch_alter_table('outfit_template', schema=None) as batch_op:
        batch_op.drop_column('style')
        batch_op.drop_column('title')

    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.drop_column('status')
        batch_op.drop_column('amount')

    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('description')
        batch_op.drop_column('name')

    with op.batch_alter_table('club', schema=None) as batch_op:
        batch_op.drop_column('name')

    with op.batch_alter_table('decoration_category', schema=None) as batch_op:
        batch_op.drop_column('description')
        batch_op.drop_column('name')
