import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect
from sqlalchemy import orm

from dila.application import structures
from dila.data import engine
from dila.data import resources


class TranslatedString(engine.Base):
    __tablename__ = 'translated_string'
    id = sqlalchemy.Column(postgres_dialect.UUID(as_uuid=True),
                           server_default=sqlalchemy.text("uuid_generate_v4()"), primary_key=True,
                           nullable=False)
    resource_pk = sqlalchemy.Column(
        postgres_dialect.UUID(as_uuid=True), sqlalchemy.ForeignKey(resources.Resource.id), nullable=False)
    resources = orm.relationship(resources.Resource, backref=orm.backref('translated_strings'))
    base_string = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    translation = sqlalchemy.Column(sqlalchemy.Text, nullable=False, default='')
    comment = sqlalchemy.Column(sqlalchemy.Text, nullable=False, default='')
    translator_comment = sqlalchemy.Column(sqlalchemy.Text, nullable=False, default='')
    context = sqlalchemy.Column(sqlalchemy.Text, nullable=False, default='')

    def as_data(self):
        return structures.TranslatedStringData(
            self.id,
            self.base_string,
            self.translation,
            self.comment,
            self.translator_comment,
            self.context,
        )


def add_translated_string(resource_pk, base_string, *, translation, comment, translator_comment, context):
    engine.session.add(TranslatedString(
        resource_pk=resource_pk, base_string=base_string, translation=translation, comment=comment,
        translator_comment=translator_comment, context=context
    ))
    engine.session.flush()


def get_translated_strings(resource_pk):
    for translated_string in TranslatedString.query.filter_by(resource_pk=resource_pk):
        yield translated_string.as_data()


def get_translated_string(pk):
    return TranslatedString.query.get(pk).as_data()


def set_translated_string(pk, **kwargs):
    update = {
        getattr(TranslatedString, key): value for key, value in kwargs.items()
    }
    TranslatedString.query.filter(TranslatedString.id == pk).update(update)
