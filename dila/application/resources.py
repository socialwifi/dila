from dila import data


def add_resource(resource_name):
    data.add_resource(resource_name)


def get_resources():
    return list(data.get_resources())


def get_resource(pk):
    return data.get_resource(pk)
