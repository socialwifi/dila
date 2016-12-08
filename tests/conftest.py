import pytest
import sh

from dila import config
from dila import data
from dila.data import engine


@pytest.fixture(scope="session")
def config_setup():
    config.setup(
        SECRET_KEY='secret',
    )


@pytest.fixture(scope="session")
def flask_app(config_setup):
    from dila.frontend.flask import wsgi
    app = wsgi.create_app()
    yield app


@pytest.fixture
def flask_client(flask_app):
    flask_app.config['WTF_CSRF_ENABLED'] = False
    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def initialized_db_autocommit_connection(postgres_server_ip):
    from dila.data import engine
    connection = engine.database.connect_with_connection('postgresql://postgres:postgres@{}/postgres'.format(postgres_server_ip))
    connection.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    engine.Base.metadata.create_all(connection)
    return connection


@pytest.fixture
def db_connection(initialized_db_autocommit_connection):
    from dila.data import engine

    connection = initialized_db_autocommit_connection
    transaction = connection.begin()
    engine.database.disable_autocommit(transaction, connection)
    engine.session.configure(bind=connection)
    yield connection
    engine.session.remove()
    transaction.rollback()
    engine.database.reenable_autocommit(transaction)


@pytest.fixture
def db_session(db_connection):
    from dila.data import engine
    session = engine.database.Session(bind=db_connection)
    yield session
    session.close()


@pytest.fixture(scope="session")
def postgres_server():
    container_name = 'test_dila_postgres'
    sh.docker('run', '-d', '--name', container_name, 'postgres')
    log = sh.docker('logs', '-f', container_name, _iter=True)
    for line in log:
        if 'PostgreSQL init process complete; ready for start up.' in line:
            break
    log.terminate()
    yield container_name
    sh.docker('rm', '-fv', container_name)


@pytest.fixture(scope="session")
def postgres_server_ip(postgres_server):
    return get_container_ip(postgres_server)


def get_container_ip(container_name):
    return sh.docker(
        'inspect', '-f', '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}', container_name).strip()
