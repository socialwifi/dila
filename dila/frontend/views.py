import flask

blueprint = flask.Blueprint('main', __name__)

@blueprint.route('/')
def home():
    return flask.render_template('home.html')
