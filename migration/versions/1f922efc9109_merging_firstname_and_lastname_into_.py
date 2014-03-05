"""Merging firstname and lastname into fullname

Revision ID: 1f922efc9109
Revises: 5145ac2c72c4
Create Date: 2013-12-01 22:43:08.097169

"""

# revision identifiers, used by Alembic.
revision = '1f922efc9109'
down_revision = '5145ac2c72c4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    print "Adding fullname column"
    op.add_column('users', sa.Column('fullname', sa.String(101)))
    
    print "Merging firstname + lastname into fullname"
    connection = op.get_bind()
    connection.execute("update users set fullname = subquery.newfullname from (select id,concat(firstname, ' ', lastname) as newfullname from users) as subquery where users.id = subquery.id", execution_options = None)

    print "Dropping firstname and lastname collumn"
    op.drop_column('users', 'firstname')
    op.drop_column('users', 'lastname')
    


def downgrade():    
    connection = op.get_bind()
    op.add_column('users', sa.Column('firstname', sa.String(101)))
    op.add_column('users', sa.Column('lastname', sa.String(101)))
    print "Simply save fullname into firstname"

    connection.execute("update users set firstname = fullname");
    
    print "Dropping fullname column"
    op.drop_column('users', 'fullname')
