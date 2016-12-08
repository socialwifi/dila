import io
from unittest import mock

test_po = '''
# My comment
#. Programmer comment
#: location.c:23
#, fuzzy
msgctxt "Disambiguation for context"
msgid "Yellow"
msgstr "Żółć"
'''


def test_home(flask_client):
    response = flask_client.get('/')
    assert '<title>Dila</title>' in response.data.decode()


def test_upload_po_file_form_visible(flask_client):
    response = flask_client.get('/')
    assert '<input id="po_file" name="po_file" type="file">' in response.data.decode()


@mock.patch('dila.application.upload_translated_po_file')
def test_upload_po_file(upload_translated_po_file, flask_client):
    response = flask_client.post(
        '/',
        data={
            'po_file': (io.BytesIO(test_po.encode()), 'test.po'),
        }
    )
    assert response.status_code == 302
    response = flask_client.get(response.location)
    assert 'File uploaded' in response.data.decode()
    upload_translated_po_file.assert_called_with(test_po)
