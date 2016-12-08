import io

test_po = '''
# My comment
#. Programmer comment
#: location.c:23
#, fuzzy
msgctxt "Disambiguation for context"
msgid "One"
msgstr "Een"
'''.encode()


def test_home(flask_client):
    response = flask_client.get('/')
    assert '<title>Dila</title>' in response.data.decode()


def test_upload_po_file(flask_client):
    response = flask_client.post(
        '/',
        data={
            'po_file': (io.BytesIO(test_po), 'test.po'),
        }
    )
    assert response.status_code == 302
    response = flask_client.get(response.location)
    assert 'File uploaded' in response.data.decode()
