import flask

from dila import application
from dila import config
from dila.frontend.flask import views


def create_app():
    app = flask.Flask(__name__)
    app.config.from_mapping(
        SERVER_NAME=config.SERVER_NAME,
        SECRET_KEY=config.SECRET_KEY,
        TESTING=config.ENV == 'test',
        DEBUG=config.DEBUG,
    )
    app.register_blueprint(views.blueprint)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        application.shutdown_session(exception=exception)
    return app
