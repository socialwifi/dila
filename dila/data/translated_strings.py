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
        base_data = self.base_string.as_data()
        return structures.TranslatedStringData(
            pk=base_data.pk,
            base_string=base_data.base_string,
            plural=base_data.plural,
            translation=self.translation,
            comment=base_data.comment,
            translator_comment=self.translator_comment,
            context=base_data.context,
            resource_pk=base_data.resource_pk,
            plural_translations=self.plural_translations_data,
        )

    @property
    def plural_translations_data(self):
        if self.plural_translated_strings:
            return self.plural_translated_strings.as_data()
        else:
            return self.base_string.empty_plural_translations_data


class PluralTranslatedString(engine.Base):
    __tablename__ = 'plural_translated_string'
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(TranslatedString.id, ondelete='CASCADE'),
                           primary_key=True)
    translated_string = orm.relationship(
        TranslatedString, backref=orm.backref('plural_translated_strings', uselist=False))
    few = sqlalchemy.Column(sqlalchemy.Text, nullable=False, default='')
    many = sqlalchemy.Column(sqlalchemy.Text, nullable=False, default='')
    other = sqlalchemy.Column(sqlalchemy.Text, nullable=False, default='')

    def as_data(self):
        return structures.PluralTranslations(
            few=self.few,
            many=self.many,
            other=self.other,
        )


def get_translated_strings(language_code, resource_pk):
    strings = list(
        base_strings.BaseString.query.filter(base_strings.BaseString.resource_pk == resource_pk)
        .order_by(base_strings.BaseString.base_string)
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


def set_translated_string(language_code, pk, *, plural_translations=None,  **kwargs):
    language = languages.Language.query.filter_by(code=language_code).one()
    try:
        translated_string = TranslatedString.query.filter(
            TranslatedString.base_string_pk == pk,
            TranslatedString.language == language
        ).one()
    except sqlalchemy.orm.exc.NoResultFound:
        translated_string = TranslatedString(base_string_pk=pk, language=language, **kwargs)
        engine.session.add(translated_string)
    else:
        for key, value in kwargs.items():
            setattr(translated_string, key, value)
    if plural_translations:
        if not translated_string.plural_translated_strings:
            translated_string.plural_translated_strings = PluralTranslatedString()
        translated_string.plural_translated_strings.few=plural_translations.few,
        translated_string.plural_translated_strings.many=plural_translations.many,
        translated_string.plural_translated_strings.other=plural_translations.other,
    engine.session.flush()
