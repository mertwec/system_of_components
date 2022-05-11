"""add row-'comment' in PCBoard and cascade-delete

Revision ID: 5e9d45473da9
Revises: 8d1041491dfa
Create Date: 2021-12-27 17:20:29.424794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e9d45473da9'
down_revision = '8d1041491dfa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('PCB', sa.Column('comment', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('PCB', 'comment')
    # ### end Alembic commands ###
