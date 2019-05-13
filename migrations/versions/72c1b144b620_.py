"""empty message

Revision ID: 72c1b144b620
Revises: 502ca34a2402
Create Date: 2019-05-11 14:01:58.231020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72c1b144b620'
down_revision = '502ca34a2402'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('login_parent_id_fkey', 'login', type_='foreignkey')
    op.create_foreign_key(None, 'login', 'users', ['parent_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint('saved_trails_user_id_fkey', 'saved_trails', type_='foreignkey')
    op.create_foreign_key(None, 'saved_trails', 'users', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'saved_trails', type_='foreignkey')
    op.create_foreign_key('saved_trails_user_id_fkey', 'saved_trails', 'users', ['user_id'], ['id'], onupdate='CASCADE', ondelete='RESTRICT')
    op.drop_constraint(None, 'login', type_='foreignkey')
    op.create_foreign_key('login_parent_id_fkey', 'login', 'users', ['parent_id'], ['id'], onupdate='CASCADE', ondelete='RESTRICT')
    # ### end Alembic commands ###