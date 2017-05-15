import flask


def check_login():
    if flask.session.get('username'):
        return None
    else:
        return flask.redirect(flask.url_for('authenticate.login'))
