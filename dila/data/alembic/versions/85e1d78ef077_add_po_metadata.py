"""Add po metadata.

Revision ID: 85e1d78ef077
Revises: deb5c1dad94a
Create Date: 2017-05-15 08:10:55.332994

"""

# revision identifiers, used by Alembic.
revision = '85e1d78ef077'
down_revision = 'deb5c1dad94a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('po_metadata',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('resource_pk', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('language_pk', sa.Integer(), nullable=False),
    sa.Column('key', sa.Text(), nullable=False),
    sa.Column('value', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['language_pk'], ['language.id'], ),
    sa.ForeignKeyConstraint(['resource_pk'], ['resource.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('resource_pk', 'language_pk', 'key', name='resource_language_key_uc')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('po_metadata')
    # ### end Alembic commands ###
