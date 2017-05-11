import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect
from sqlalchemy import orm

from dila.application import structures
from dila.data import engine, base_strings
from dila.data import languages


class TranslatedString(engine.Base):
    __tablename__ = 'translated_string'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    base_string_pk = sqlalchemy.Column(
        postgres_dialect.UUID(as_uuid=True),
        sqlalchemy.ForeignKey(base_strings.BaseString.id, ondelete='CASCADE'),
        nullable=False)
    base_string = orm.relationship(
        base_strings.BaseString, backref=orm.backref('translated_strings'))
    language_pk = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(languages.Language.id), nullable=False)
    language = orm.relationship(languages.Language, backref=orm.backref('translated_strings'))
    translation = sqlalchemy.Column(sqlalchemy.Text, nullable=False, default='')
    translator_comment = sqlalchemy.Column(sqlalchemy.Text, nullable=False, default='')
    __table_args__ = (
        sqlalchemy.UniqueConstraint('base_string_pk', 'language_pk', name='base_string_language_uc'),
    )

    def as_data(self):
        return structures.TranslatedStringData(
            self.base_string.id,
            self.base_string.base_string,
            self.translation,
            self.base_string.comment,
            self.translator_comment,
            self.base_string.context,
            self.base_string.resource_pk,
        )


def get_translated_strings(language_code, resource_pk):
    strings = list(
        base_strings.BaseString.query.filter(base_strings.BaseString.resource_pk == resource_pk)
    )
    base_string_ids = (string.id for string in strings)
    translated_strings = TranslatedString.query.join(TranslatedString.language).filter(
        TranslatedString.base_string_pk.in_(base_string_ids), languages.Language.code == language_code
    )
    translated_string_map = {string.base_string_pk: string for string in translated_strings}
    for string in strings:
        yield translated_string_map.get(string.id, string).as_data()


def get_translated_string(language_code, pk):
    try:
        return TranslatedString.query.join(TranslatedString.language).filter(
            TranslatedString.base_string_pk == pk, languages.Language.code == language_code).one().as_data()
    except sqlalchemy.orm.exc.NoResultFound:
        return base_strings.BaseString.query.filter_by(id=pk).one().as_data()


def set_translated_string(language_code, pk, **kwargs):
    language = languages.Language.query.filter_by(code=language_code).one()
    try:
        existing = TranslatedString.query.filter(
            TranslatedString.base_string_pk == pk,
            TranslatedString.language == language
        ).one()
    except sqlalchemy.orm.exc.NoResultFound:
        engine.session.add(TranslatedString(
            base_string_pk=pk, language=language, **kwargs
        ))
    else:
        for key, value in kwargs.items():
            setattr(existing, key, value)
    engine.session.flush()
