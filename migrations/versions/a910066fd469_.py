"""empty message

Revision ID: a910066fd469
Revises: ea726b6303a4
Create Date: 2018-08-24 08:47:24.350345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a910066fd469'
down_revision = 'ea726b6303a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('_ulikes', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', '_ulikes')
    # ### end Alembic commands ###
