"""empty message

Revision ID: 27f96a9e2845
Revises: dbb37683a088
Create Date: 2021-04-30 10:44:05.000394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27f96a9e2845'
down_revision = 'dbb37683a088'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
