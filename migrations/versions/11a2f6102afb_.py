"""empty message

Revision ID: 11a2f6102afb
Revises: 21e08634e678
Create Date: 2019-05-10 12:04:29.424737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11a2f6102afb'
down_revision = '21e08634e678'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('saved_trails', sa.Column('trail_data', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('saved_trails', 'trail_data')
    # ### end Alembic commands ###
