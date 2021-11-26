"""Add table:PCB, and associated with components

Revision ID: 316757c956a5
Revises: 06f4a4dee8a6
Create Date: 2021-11-24 14:35:14.486016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '316757c956a5'
down_revision = '06f4a4dee8a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('component_pcb',
    sa.Column('pcb_id', sa.Integer(), nullable=False),
    sa.Column('comp_id', sa.Integer(), nullable=False),
    sa.Column('comp_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['comp_id'], ['components.id'], ),
    sa.ForeignKeyConstraint(['pcb_id'], ['PCB.id'], ),
    sa.PrimaryKeyConstraint('pcb_id', 'comp_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('component_pcb')
    # ### end Alembic commands ###