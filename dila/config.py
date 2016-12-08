SERVER_NAME = None
SECRET_KEY = None
ENV = 'production'


def setup(**mapping):
    globals().update(mapping)
