from dila import data


def setup():
    data.setup()


def shutdown_session(exception=None):
    data.shutdown_session(exception=exception)
