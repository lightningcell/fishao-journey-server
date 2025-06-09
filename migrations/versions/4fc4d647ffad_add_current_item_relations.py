"""Add player's current bait and rod item relations

Revision ID: 4fc4d647ffad
Revises: 65e668ad3010
Create Date: 2025-06-04 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4fc4d647ffad'
down_revision = '65e668ad3010'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_bait_item_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('current_rod_item_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_player_current_bait_item', 'item', ['current_bait_item_id'], ['id'])
        batch_op.create_foreign_key('fk_player_current_rod_item', 'item', ['current_rod_item_id'], ['id'])


def downgrade():
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.drop_constraint('fk_player_current_bait_item', type_='foreignkey')
        batch_op.drop_constraint('fk_player_current_rod_item', type_='foreignkey')
        batch_op.drop_column('current_bait_item_id')
        batch_op.drop_column('current_rod_item_id')
