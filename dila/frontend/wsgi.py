import flask

from dila import config


def create_app():
    app = flask.Flask(__name__)
    app.config.from_mapping(
        SERVER_NAME=config.SERVER_NAME,
        SECRET_KEY=config.SECRET_KEY,
        TESTING=config.ENV == 'test',
    )
    return app
