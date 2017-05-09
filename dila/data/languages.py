import uuid

import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect

from dila.application import structures
from dila.data import engine


class Language(engine.Base):
    __tablename__ = 'language'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)
    code = sqlalchemy.Column(sqlalchemy.Text(), nullable=False, unique=True)

    def as_data(self):
        return structures.Language(code=self.code, name=self.name)


def add_language(name, code):
    language = Language(name=name, code=code)
    engine.session.add(language)
    engine.session.flush()
    return language.as_data()


def get_language(code):
    return Language.query.filter_by(code=code).one().as_data()


def get_languages():
    for language in Language.query.all():
        yield language.as_data()
