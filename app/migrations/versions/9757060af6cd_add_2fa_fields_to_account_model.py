"""Add 2FA fields to Account model

Revision ID: 9757060af6cd
Revises: 2098ebea90d6
Create Date: 2025-06-22 14:15:07.408794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9757060af6cd'
down_revision = '2098ebea90d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.add_column(sa.Column('totp_secret', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('backup_codes', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.drop_column('backup_codes')
        batch_op.drop_column('totp_secret')

    # ### end Alembic commands ###
