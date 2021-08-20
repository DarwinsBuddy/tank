from os import path

_ROOT = path.abspath(path.dirname(__file__))


def get_data(relative_path):
    return path.join(_ROOT, 'data', relative_path)
