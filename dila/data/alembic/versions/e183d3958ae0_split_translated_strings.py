"""Split translated strings

Revision ID: e183d3958ae0
Revises: 7742ac8b1599
Create Date: 2017-05-11 08:18:47.142734

"""

# revision identifiers, used by Alembic.
revision = 'e183d3958ae0'
down_revision = '7742ac8b1599'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('base_string',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('resource_pk', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('base_string', sa.Text(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=False),
    sa.Column('context', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['resource_pk'], ['resource.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('translated_string')
    op.create_table('translated_string',
    sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
    sa.Column('base_string_pk', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('language_pk', sa.Integer, nullable=False),
    sa.Column('translation', sa.Text(), nullable=False),
    sa.Column('translator_comment', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['base_string_pk'], ['base_string.id'], ),
    sa.ForeignKeyConstraint(['language_pk'], ['language.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('base_string_pk', 'language_pk', name='base_string_language_uc'),
    )


def downgrade():
    op.drop_table('translated_string')
    op.create_table('translated_string',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), autoincrement=False, nullable=False),
    sa.Column('base_string', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('translation', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('comment', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('translator_comment', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('context', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('resource_pk', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['resource_pk'], ['resource.id'], name='translated_string_resource_pk_fkey'),
    sa.PrimaryKeyConstraint('id', name='translated_string_pkey')
    )
    op.drop_table('base_string')
