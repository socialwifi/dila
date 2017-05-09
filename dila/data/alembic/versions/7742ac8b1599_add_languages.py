"""Add languages

Revision ID: 7742ac8b1599
Revises: 04d870437e14
Create Date: 2017-05-09 14:10:25.598265

"""

# revision identifiers, used by Alembic.
revision = '7742ac8b1599'
down_revision = '04d870437e14'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('language',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('code', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )


def downgrade():
    op.drop_table('language')
