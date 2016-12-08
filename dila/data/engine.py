import sqlalchemy.ext.declarative
import sqlalchemy.orm

from dila.data import postgres_autocommit
from dila import config


database = postgres_autocommit.Database()
session = sqlalchemy.orm.scoped_session(database.Session)
Base = sqlalchemy.ext.declarative.declarative_base()
Base.query = session.query_property()

def setup():
    database.connect(config.DATABASE_URL)
