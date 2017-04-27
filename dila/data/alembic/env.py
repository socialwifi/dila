from __future__ import with_statement
from alembic import context
from logging.config import fileConfig
import sqlalchemy.pool
import sqlalchemy.engine

from dila.data import engine
from dila import config as dila_config

from dila.frontend import initialize

__import__('dila.data.translated_strings')
initialize.initialize()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = engine.Base.metadata


def run_migrations_offline():
    context.configure(
        url=dila_config.DATABASE_URL, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = sqlalchemy.engine.create_engine(
        dila_config.DATABASE_URL,
        poolclass=sqlalchemy.pool.NullPool
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
