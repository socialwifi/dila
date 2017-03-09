import flask
from cached_property import cached_property
from flask import views

from dila import application
from dila.frontend.flask import forms

blueprint = flask.Blueprint('main', __name__)


class HomeView(views.MethodView):
    def get(self):
        return flask.render_template('home.html', **self.context)

    def post(self):
        if self.form.validate():
            application.upload_translated_po_file(flask.request.files[self.form.po_file.name].read().decode())
            flask.flash('File uploaded')
            return flask.redirect(flask.url_for('main.home'))
        else:
            return self.get()

    @property
    def context(self):
        return {
            'translated_strings': self.translated_strings,
            'form': self.form
        }

    @cached_property
    def form(self):
        return forms.PoFileUpload()

    @cached_property
    def translated_strings(self):
        return application.get_translated_strings()

blueprint.add_url_rule('/', view_func=HomeView.as_view('home'))


class TranslatedStringEditor(views.MethodView):
    def get(self, pk):
        return flask.render_template('layout.html')

blueprint.add_url_rule('/<pk>/', view_func=TranslatedStringEditor.as_view('translated_string'))
