"""Adding currently_live_in field

Revision ID: 5145ac2c72c4
Revises: None
Create Date: 2013-12-01 08:55:53.588715

"""

# revision identifiers, used by Alembic.
revision = '5145ac2c72c4'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('users', sa.Column('currently_live_in', sa.String(length=300), nullable=True))

def downgrade():
    op.drop_column('users', 'currently_live_in')
