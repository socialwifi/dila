SERVER_NAME = None
SECRET_KEY = None
ENV = 'production'
DEBUG = False


def setup(**mapping):
    globals().update(mapping)
