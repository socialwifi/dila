"""Add base_string unique constraint.

Revision ID: 558950f05825
Revises: e183d3958ae0
Create Date: 2017-05-11 13:03:30.866815

"""

# revision identifiers, used by Alembic.
revision = '558950f05825'
down_revision = 'e183d3958ae0'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_unique_constraint('resource_base_string_context_uc', 'base_string', ['resource_pk', 'base_string', 'context'])


def downgrade():
    op.drop_constraint('resource_base_string_context_uc', 'base_string', type_='unique')
