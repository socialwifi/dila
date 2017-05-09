import flask

from dila.frontend.flask import forms

def get_new_form():
    return forms.NewLanguageForm(obj={'next': flask.request.url})
