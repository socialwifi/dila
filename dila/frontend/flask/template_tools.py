import urllib.parse

import flask

from dila import config


def setup_app(app):

    @app.template_global()
    def static_url(filename):
        if config.STATIC_URL:
            return urllib.parse.urljoin(config.STATIC_URL, filename)
        return flask.url_for('static', filename=filename)
