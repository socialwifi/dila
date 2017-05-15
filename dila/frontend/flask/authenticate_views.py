import flask
from flask import views

from dila.frontend.flask import template_tools

blueprint = flask.Blueprint('authenticate', __name__)
template_tools.setup_language_context(blueprint)


class LoginView(views.MethodView):
    def get(self):
        return flask.render_template('login.html', **self.context)


blueprint.add_url_rule('/login/', view_func=LoginView.as_view('login'))
