import shutil
from importlib import resources
from importlib.resources import files

DATA_PACKAGE = 'rc3.data'
SCHEMA_BASE_URL = "http://localhost:8000"
SCHEMA_PREFIX = "rc3"
SCHEMA_VERSION = "0.0.3"
COLLECTION_FILENAME = "rc-collection.json"
FOLDER_FILENAME = "rc-folder.json"
SETTINGS_FILENAME = "rc-settings.json"
GLOBAL_ENV_FILENAME = "rc-global.json"
VERSION_MAP = {
    'auth': SCHEMA_VERSION,
    'collection': SCHEMA_VERSION,
    'environment': SCHEMA_VERSION,
    'folder': SCHEMA_VERSION,
    'request': '0.0.9',
    'settings': SCHEMA_VERSION
}

def get_file(filename):
    return files(DATA_PACKAGE).joinpath(filename)


def get_schema_file(partial):
    return get_file(f'home/schemas/{SCHEMA_PREFIX}-{partial}-{VERSION_MAP.get(partial,SCHEMA_VERSION)}.json')


def copy_tree(source_file, dest):
    source = get_file(source_file)
    with resources.as_file(source) as path:
        shutil.copytree(path, dest, dirs_exist_ok=True)


def copy(source_file, dest):
    source = get_file(source_file)
    with resources.as_file(source) as path:
        shutil.copy(path, dest)
