import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect
from sqlalchemy import orm

from dila.data import engine
from dila.data import languages
from dila.data import resources


class PoMetadataEntry(engine.Base):
    __tablename__ = 'po_metadata'
    id = sqlalchemy.Column(postgres_dialect.UUID(as_uuid=True),
                           server_default=sqlalchemy.text("uuid_generate_v4()"), primary_key=True,
                           nullable=False)
    resource_pk = sqlalchemy.Column(
        postgres_dialect.UUID(as_uuid=True), sqlalchemy.ForeignKey(resources.Resource.id), nullable=False)
    resource = orm.relationship(resources.Resource, backref=orm.backref('po_metadata'))
    language_pk = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(languages.Language.id), nullable=False)
    language = orm.relationship(languages.Language, backref=orm.backref('po_metadata'))
    key = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    value = sqlalchemy.Column(sqlalchemy.Text, nullable=False, default='')
    __table_args__ = (
        sqlalchemy.UniqueConstraint('resource_pk', 'language_pk', 'key', name='resource_language_key_uc'),
    )


def update_po_metadata(language_code, resource_pk, metadata):
    language = languages.Language.query.filter_by(code=language_code).one()
    for key, value in metadata.items():
        try:
            entry = PoMetadataEntry.query.filter(
                PoMetadataEntry.resource_pk == resource_pk,
                PoMetadataEntry.language == language,
                PoMetadataEntry.key == key,
            ).one()
        except sqlalchemy.orm.exc.NoResultFound:
            entry = PoMetadataEntry(resource_pk=resource_pk, language=language, key=key, value=value)
            engine.session.add(entry)
        else:
            entry.value = value
        engine.session.flush()


def get_po_metadata(language_code, resource_pk):
    po_metadata_entries = PoMetadataEntry.query.join(PoMetadataEntry.language).filter(
        PoMetadataEntry.resource_pk == resource_pk, languages.Language.code == language_code
    ).order_by(PoMetadataEntry.key)
    result = {}
    for entry in po_metadata_entries:
        result[entry.key] = entry.value
    return result
