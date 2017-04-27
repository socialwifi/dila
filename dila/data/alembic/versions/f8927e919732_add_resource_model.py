"""Add resource model.

Revision ID: f8927e919732
Revises: 58e7f2fc7ff7
Create Date: 2017-04-27 10:07:33.766861

"""

# revision identifiers, used by Alembic.
revision = 'f8927e919732'
down_revision = '58e7f2fc7ff7'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.create_table('resource',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('translated_string', sa.Column('resource_pk', postgresql.UUID(as_uuid=True), nullable=False))
    op.create_foreign_key(None, 'translated_string', 'resource', ['resource_pk'], ['id'])


def downgrade():
    op.drop_constraint(None, 'translated_string', type_='foreignkey')
    op.drop_column('translated_string', 'resource_pk')
    op.drop_table('resource')
