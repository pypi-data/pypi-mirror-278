import os

from ruamel.yaml import YAML

from .utils import error, warn, info, fix_line

def read_yaml_file(file):
    yaml = YAML()
    with open(file, 'r') as f:
        config = yaml.load(f)

    return config

def read_yaml_config(configs_path, keyword=None):
    yaml = YAML()
    yaml_config = {}

    file_path = None
    directory_path = configs_path
    if keyword is not None:
        file_path = f"{configs_path}/{keyword}.yaml"
        directory_path = f"{configs_path}/{keyword}"

        if os.path.isfile(file_path) and os.path.isdir(directory_path):
            warn(f"the file and directory both exist; prioritize using the file: {file_path}")

    # check if file exists
    if file_path is not None and os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            config = yaml.load(f)

        yaml_config[f"{keyword}.yaml"] = config
        return yaml_config

    res = dict()
    # check if directory exists
    if os.path.isdir(directory_path):
        for filename in os.listdir(directory_path):
            if filename.endswith('.yaml'):
                full_path = os.path.join(directory_path, filename)
                with open(full_path, 'r') as f:
                    yaml_config[filename] = yaml.load(f)
        return yaml_config

    # not found
    return None

def read_lua_modules(configs_path, folder):
    folder = f"{configs_path}/{folder}"
    if not os.path.isdir(folder):
        error(f"lua module folder not found: {folder}")

    lua_files_content = {}
    for filename in os.listdir(folder):
        if filename.endswith('.lua'):
            file_key = os.path.splitext(filename)[0]
            file_path = os.path.join(folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                lua_files_content[file_key] = file.read()

    return lua_files_content
