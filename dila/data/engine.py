import sqlalchemy.ext.declarative
import sqlalchemy.orm

from sqlalchemy_postgres_autocommit import databases
from dila import config


database = databases.Database()
session = sqlalchemy.orm.scoped_session(database.Session)
Base = sqlalchemy.ext.declarative.declarative_base()
Base.query = session.query_property()


def setup():
    database.connect(config.DATABASE_URL)


def shutdown_session(exception=None):
    session.remove()
