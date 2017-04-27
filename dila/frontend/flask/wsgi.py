import urllib.parse

import flask

from dila import application
from dila import config
from dila.frontend import initialize
from dila.frontend.flask import views


def main(initialized=False):
    if not initialized:
        initialize.initialize()
    app = create_app()

    prepare_application(app)
    return app


def prepare_application(app):
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        application.shutdown_session(exception=exception)


def create_app():
    app = flask.Flask(__name__)
    app.config.from_mapping(
        SERVER_NAME=config.SERVER_NAME,
        SECRET_KEY=config.SECRET_KEY,
        TESTING=config.ENV == 'test',
        DEBUG=config.DEBUG,
    )
    app.register_blueprint(views.blueprint)

    @app.template_global()
    def static_url(filename):
        if config.STATIC_URL:
            return urllib.parse.urljoin(config.STATIC_URL, filename)

        return flask.url_for('static', filename=filename)

    return app
