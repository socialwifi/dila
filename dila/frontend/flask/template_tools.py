import urllib.parse

import flask

from dila import config
from dila.frontend.flask import languages
from dila.frontend.flask import user_tools


def setup_app(app):
    @app.template_global()
    def static_url(filename):
        if config.STATIC_URL:
            return urllib.parse.urljoin(config.STATIC_URL, filename)
        return flask.url_for('static', filename=filename)


def setup_language_context(blueprint):
    @blueprint.context_processor
    def inject_languages_menu():
        return {
            'languages_form': languages.get_new_form(),
            'languages_links': list(languages.get_language_links()),
            'current_language_code': languages.current_language_code(),
            'current_language': languages.current_language(),
        }


def setup_user_context(blueprint):
    @blueprint.context_processor
    def inject_curren_user_menu():
        return {
            'current_user': user_tools.current_user(),
        }
