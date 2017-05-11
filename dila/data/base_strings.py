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

    def as_data(self):
        return structures.TranslatedStringData(
            pk=self.id,
            base_string=self.base_string,
            translation='',
            comment=self.comment,
            translator_comment='',
            context=self.context,
            resource_pk=self.resource_pk,
        )


def add_translated_string(resource_pk, base_string, *, comment, context):
    translated_string = BaseString(
        resource_pk=resource_pk, base_string=base_string, comment=comment, context=context
    )
    engine.session.add(translated_string)
    engine.session.flush()
    return translated_string.id

