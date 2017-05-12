import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect
from sqlalchemy import orm

from dila.application import structures
from dila.data import engine
from dila.data import resources


class BaseString(engine.Base):
    __tablename__ = 'base_string'
    id = sqlalchemy.Column(postgres_dialect.UUID(as_uuid=True),
                           server_default=sqlalchemy.text("uuid_generate_v4()"), primary_key=True,
                           nullable=False)
    resource_pk = sqlalchemy.Column(
        postgres_dialect.UUID(as_uuid=True), sqlalchemy.ForeignKey(resources.Resource.id), nullable=False)
    resources = orm.relationship(resources.Resource, backref=orm.backref('translated_strings'))
    base_string = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    comment = sqlalchemy.Column(sqlalchemy.Text, nullable=False, default='')
    context = sqlalchemy.Column(sqlalchemy.Text, nullable=False, default='')
    plural = sqlalchemy.Column(sqlalchemy.Text, nullable=False, default='')
    __table_args__ = (
        sqlalchemy.UniqueConstraint('resource_pk', 'base_string', 'context', name='resource_base_string_context_uc'),
    )

    def as_data(self):
        return structures.TranslatedStringData(
            pk=self.id,
            base_string=self.base_string,
            plural=self.plural,
            translation='',
            comment=self.comment,
            translator_comment='',
            context=self.context,
            resource_pk=self.resource_pk,
            plural_translations=self.empty_plural_translations_data,
        )

    @property
    def empty_plural_translations_data(self):
        if self.plural:
            return structures.PluralTranslations(few='', many='', other='')
        else:
            return None


def add_or_update_base_string(resource_pk, base_string, *, comment, context, plural=''):
    try:
        base_string = BaseString.query.filter(
            BaseString.resource_pk == resource_pk,
            BaseString.base_string == base_string,
            BaseString.context == (context or ''),
        ).one()
    except sqlalchemy.orm.exc.NoResultFound:
        base_string = BaseString(resource_pk=resource_pk, base_string=base_string, comment=comment, context=context,
                                 plural=plural)
        engine.session.add(base_string)
    else:
        base_string.comment = comment
        base_string.plural = plural
    engine.session.flush()
    return base_string.id


def delete_old_strings(resource_pk, *, keep_pks):
    BaseString.query.filter(
        BaseString.resource_pk == resource_pk,
        BaseString.id.notin_(keep_pks),
    ).delete(synchronize_session='fetch')
