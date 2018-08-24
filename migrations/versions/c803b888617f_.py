"""empty message

Revision ID: c803b888617f
Revises: 57a6f0db6221
Create Date: 2018-08-22 01:20:45.644411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c803b888617f'
down_revision = '57a6f0db6221'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('admin_token_admin_id_fkey', 'admin_token', type_='foreignkey')
    op.create_foreign_key(None, 'admin_token', 'admin', ['admin_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'admin_token', type_='foreignkey')
    op.create_foreign_key('admin_token_admin_id_fkey', 'admin_token', 'user', ['admin_id'], ['id'])
    # ### end Alembic commands ###