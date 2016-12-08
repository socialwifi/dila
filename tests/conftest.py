import pytest

from dila.frontend.flask import wsgi


@pytest.fixture(scope="session")
def flask_app():
    app = wsgi.create_app()
    yield app


@pytest.fixture
def flask_client(flask_app):
    with flask_app.test_client() as client:
        yield client
