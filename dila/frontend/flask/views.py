import flask
from flask import views

from dila.frontend.flask import forms

blueprint = flask.Blueprint('main', __name__)


class HomeView(views.MethodView):
    def get(self):
        return flask.render_template('home.html', **self.context)

    def post(self):
        if self.form.validate():
            flask.flash('File uploaded')
            return flask.redirect(flask.url_for('main.home'))
        else:
            return self.get()

    @property
    def context(self):
        return {
            'form': self.form
        }

    @property
    def form(self):
        return forms.PoFileUpload()

blueprint.add_url_rule('/', view_func=HomeView.as_view('home'))
