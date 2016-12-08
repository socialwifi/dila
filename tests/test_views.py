from dila.frontend import views


def test_home(flask_app):
    with flask_app.app_context():
        response = views.home()
    assert '<title>Dila</title>' in response
