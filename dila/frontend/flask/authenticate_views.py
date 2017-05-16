import flask
from cached_property import cached_property
from flask import views

from dila.frontend.flask import user_tools
from dila.frontend.flask import forms

blueprint = flask.Blueprint('authenticate', __name__)


class LoginView(views.MethodView):
    def get(self):
        return flask.render_template('login.html', **self.context)

    def post(self):
        if self.form.validate():
            user_tools.set_current_user(self.form.user)
            return flask.redirect(flask.url_for('main.home'))
        else:
            return self.get()


    @property
    def context(self):
        return {
            'form': self.form,
        }

    @cached_property
    def form(self):
        return forms.LoginForm()


blueprint.add_url_rule('/login/', view_func=LoginView.as_view('login'))


class LogoutView(views.MethodView):
    def post(self):
        user_tools.logout()
        return flask.redirect(flask.url_for('authenticate.login'))

blueprint.add_url_rule('/logout/', view_func=LogoutView.as_view('logout'))
