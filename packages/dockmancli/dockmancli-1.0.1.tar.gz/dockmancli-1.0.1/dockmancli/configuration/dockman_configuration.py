#!/usr/bin/env python3
import os

import docker
import yaml
from InquirerPy.base import Choice
from dockmancli.utils import prompt_utils
from dockmancli.utils.emjois import Emjois
from dockmancli.dockman_docker.docker_common import DockerCommon


class Configuration(DockerCommon):

    def __init__(self):
        super().__init__()
        self.client = docker.from_env()

    def main_options(self):
        selected_option = None
        while selected_option != prompt_utils.MENU_OPTION_BACK:
            choices = [
                Choice('config', name=f'{Emjois.ICON_YAML} Create images, containers, volumes and/or networks')
            ]

            selected_option = prompt_utils.option_select('Configuration options', choices)

            if selected_option == 'config':
                self.__read_yaml()

    def __read_yaml(self):
        home_path = os.path.expanduser('~')
        yaml_path = prompt_utils.filepath('Select yaml configuration file', mandatory=False, default_path=home_path)

        if yaml_path:
            with open(yaml_path, 'r') as file:
                images_containers_config = yaml.safe_load(file)

            if 'images' in images_containers_config or 'containers' in images_containers_config:
                if 'images' in images_containers_config:
                    self._create_images(images_containers_config['images'])
                if 'networks' in images_containers_config:
                    self._create_networks(images_containers_config['networks'])
                if 'volumes' in images_containers_config:
                    self._create_volumes(images_containers_config['volumes'])
                if 'containers' in images_containers_config:
                    self._create_containers(images_containers_config['containers'])
            else:
                prompt_utils.error_message('Yaml has not "images" or "containers" key')
