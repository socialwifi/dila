import flask
from dila import application
from dila.application import structures

def check_login():
    if current_user().authenticated:
        return None
    else:
        return flask.redirect(flask.url_for('authenticate.login'))


def logout():
    set_current_user(application.ANONYMOUS_USER)


def set_current_user(user, session=None):
    session = flask.session if session is None else session
    session['user'] = user._asdict()


def current_user():
    user_dict = flask.session.get('user', {})
    for field in application.ANONYMOUS_USER._fields:
        user_dict.setdefault(field, getattr(application.ANONYMOUS_USER, field))
    return structures.User(**user_dict)
