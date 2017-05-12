"""Add plural base string.

Revision ID: 71f4f6391672
Revises: 4ce05ae50d01
Create Date: 2017-05-12 09:14:24.296708

"""

# revision identifiers, used by Alembic.
revision = '71f4f6391672'
down_revision = '4ce05ae50d01'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('base_string', sa.Column('plural', sa.Text(), nullable=True))
    op.execute("UPDATE base_string SET plural='' WHERE plural is NULL")
    op.alter_column('base_string', 'plural',
                    existing_type=sa.TEXT(),
                    nullable=False)


def downgrade():
    op.drop_column('base_string', 'plural')
