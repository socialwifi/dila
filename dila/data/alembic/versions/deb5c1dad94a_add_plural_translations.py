"""Add plural translations.

Revision ID: deb5c1dad94a
Revises: 71f4f6391672
Create Date: 2017-05-12 12:07:01.259819

"""

# revision identifiers, used by Alembic.
revision = 'deb5c1dad94a'
down_revision = '71f4f6391672'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('plural_translated_string',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('few', sa.Text(), nullable=False),
    sa.Column('many', sa.Text(), nullable=False),
    sa.Column('other', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['translated_string.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('plural_translated_string')
