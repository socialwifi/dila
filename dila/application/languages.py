from dila import data


def add_language(name, code):
    data.add_language(name, code)


def get_languages():
    return list(data.get_languages())


def get_language(code):
    return data.get_language(code)
