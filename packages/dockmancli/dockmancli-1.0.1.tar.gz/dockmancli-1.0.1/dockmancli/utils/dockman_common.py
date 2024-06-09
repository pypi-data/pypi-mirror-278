#!/usr/bin/env python3
import os
import yaml
from . import prompt_utils


def read_yaml(key: str, function):
    home_path = os.path.expanduser('~')
    yaml_path = prompt_utils.filepath('Select yaml configuration file', mandatory=False, default_path=home_path)

    if yaml_path:
        if not os.path.isabs(yaml_path):
            actual_path = os.path.dirname(__file__)
            yaml_path = os.path.join(actual_path, yaml_path)

        with open(yaml_path, 'r') as file:
            config_file = yaml.safe_load(file)

        if key in config_file:
            function(config_file[key])
        else:
            prompt_utils.error_message(f'Yaml has not "{key}" key')
