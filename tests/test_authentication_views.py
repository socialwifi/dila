import re
from unittest import mock

from dila.application import structures


def test_login_form(flask_client):
    response = flask_client.get('/login/')
    assert re.search('<input class="[^"]*" id="username" name="username" type="text" value="">',
                     response.data.decode())
    assert re.search('<input class="[^"]*" id="password" name="password" type="password" value="">',
                     response.data.decode())
    assert re.search('<input class="[^"]*" id="login" value="Log in" type="submit">', response.data.decode())


@mock.patch('dila.application.authenticate')
def test_post_login(authenticate, flask_client):
    authenticate.return_value = structures.User(
        authenticated=True,
        username='username',
        first_name='Sheldon',
        last_name='Cooper',
    )
    response = flask_client.post('/login/', data={'username': 'songo', 'password': 'ssj4'})
    authenticate.assert_called_once_with('songo', 'ssj4')
    assert response.status_code == 302
    assert response.location == 'http://localhost/'


@mock.patch('dila.application.authenticate')
def test_post_invalid_login(authenticate, flask_client):
    authenticate.return_value = structures.User(
        authenticated=False,
        username='',
        first_name='',
        last_name='',
    )
    response = flask_client.post('/login/', data={'username': 'songo', 'password': 'ssj5'})
    authenticate.assert_called_once_with('songo', 'ssj5')
    assert "Invalid login or password" in response.data.decode()
