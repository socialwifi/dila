import pytest

from dila import config
from dila.frontend.flask import wsgi


@pytest.fixture(scope="session")
def config_setup():
    config.setup(
        SECRET_KEY='secret',
    )


@pytest.fixture(scope="session")
def flask_app(config_setup):
    app = wsgi.create_app()
    yield app


@pytest.fixture
def flask_client(flask_app):
    flask_app.config['WTF_CSRF_ENABLED'] = False
    with flask_app.test_client() as client:
        yield client
