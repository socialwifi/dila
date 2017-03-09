import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect

from dila.application import structures
from dila.data import engine


class TranslatedString(engine.Base):
    __tablename__ = 'translated_string'
    id = sqlalchemy.Column(postgres_dialect.UUID(as_uuid=True),
                           server_default=sqlalchemy.text("uuid_generate_v4()"), primary_key=True,
                           nullable=False)
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


def add_translated_string(base_string, *, translation, comment, translator_comment, context):
    engine.session.add(TranslatedString(
        base_string=base_string, translation=translation, comment=comment, translator_comment=translator_comment,
        context=context
    ))
    engine.session.flush()


def get_translated_strings():
    for translated_string in TranslatedString.query.all():
        yield translated_string.as_data()


def get_translated_string(pk):
    return TranslatedString.query.get(pk).as_data()
