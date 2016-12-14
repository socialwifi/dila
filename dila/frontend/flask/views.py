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
            'form': self.form
        }

    @cached_property
    def form(self):
        return forms.PoFileUpload()

blueprint.add_url_rule('/', view_func=HomeView.as_view('home'))
