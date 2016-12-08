import pytest

from dila.frontend import wsgi


@pytest.fixture(scope="session")
def flask_app():
    app = wsgi.create_app()
    yield app
