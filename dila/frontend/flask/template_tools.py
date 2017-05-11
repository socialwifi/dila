import urllib.parse

import flask

from dila import config
from dila.frontend.flask import languages


def setup_app(app):

    @app.template_global()
    def static_url(filename):
        if config.STATIC_URL:
            return urllib.parse.urljoin(config.STATIC_URL, filename)
        return flask.url_for('static', filename=filename)

    @app.context_processor
    def inject_languages_menu():
        return {
            'languages_form': languages.get_new_form(),
            'languages_links': list(languages.get_language_links()),
            'current_language_code': languages.current_language_code(),
            'current_language': languages.current_language(),
        }
