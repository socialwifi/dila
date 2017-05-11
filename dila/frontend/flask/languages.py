import flask

from dila.frontend.flask import forms
from dila import application


def get_new_form():
    return forms.NewLanguageForm(next=flask.request.path)


def get_language_links():
    for language in application.get_languages():
        view_args = dict(flask.request.view_args, language_code=language.code)
        yield (language.name, flask.url_for(flask.request.endpoint, **view_args))


def current_language_code():
    return (flask.request.view_args or {}).get('language_code')


def current_language():
    code = current_language_code()
    if code:
        return application.get_language(code).name
    else:
        return None
