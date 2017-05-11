"""Add on delete cascade to postgres.

Revision ID: 4ce05ae50d01
Revises: 558950f05825
Create Date: 2017-05-11 14:07:10.401257

"""

# revision identifiers, used by Alembic.
revision = '4ce05ae50d01'
down_revision = '558950f05825'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint('translated_string_base_string_pk_fkey', 'translated_string', type_='foreignkey')
    op.create_foreign_key(None, 'translated_string', 'base_string', ['base_string_pk'], ['id'], ondelete='CASCADE')


def downgrade():
    op.drop_constraint(None, 'translated_string', type_='foreignkey')
    op.create_foreign_key('translated_string_base_string_pk_fkey', 'translated_string', 'base_string', ['base_string_pk'], ['id'])
