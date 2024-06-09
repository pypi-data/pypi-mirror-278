#!/usr/bin/env python3
import docker
from InquirerPy.base import Choice
from dockmancli.utils import prompt_utils
from dockmancli.utils.emjois import Emjois
from dockmancli.utils.dockman_common import read_yaml
from dockmancli.dockman_docker.docker_common import DockerCommon


class DockManVolume(DockerCommon):

    def __init__(self):
        super().__init__()
        self.client = docker.from_env()

    def main_options(self):
        selected_option = None
        while selected_option != prompt_utils.MENU_OPTION_BACK:
            choices = [
                Choice('list', name=f'{Emjois.ICON_LIST} List'),
                Choice('create', name=f'{Emjois.ICON_NEW} Create')
            ]

            selected_option = prompt_utils.option_select('Volume options:', choices)

            if selected_option == 'list':
                self.__list()
            elif selected_option == 'create':
                self.__create()

    def __list(self):
        selected_option = None
        while selected_option != prompt_utils.MENU_OPTION_BACK:
            volumes = self.__get_volumes()
            selected_option = prompt_utils.option_select('Select volume', volumes)

            if selected_option != prompt_utils.MENU_OPTION_BACK:
                self.__volume_options(selected_option)

    def __volume_options(self, volume_id):
        choices = [
            Choice('reload', name=f'{Emjois.ICON_RESTART} Reload'),
            Choice('remove', name=f'{Emjois.ICON_REMOVE} Remove')
        ]

        action = prompt_utils.option_select(f'Volume options', choices)
        if action == 'remove':
            yes = prompt_utils.confirm_choices()

        try:
            if action == 'reload':
                self.__reload(volume_id)
            elif action == 'remove':
                if yes:
                    self.__remove(volume_id)
        except docker.errors.APIError as e:
            prompt_utils.error_message(str(e))

    def __reload(self, volume_id):
        volume = self.client.volumes.get(volume_id)
        volume.reload()
        prompt_utils.info_message(f'Volume "{volume.name}" reloaded')

    def __remove(self, volume_id):
        volume = self.client.volumes.get(volume_id)
        volume.remove()
        prompt_utils.info_message(f'Volume "{volume.name}" removed')

    def __create(self):
        selected_option = None
        while selected_option != prompt_utils.MENU_OPTION_BACK:
            choices = [
                Choice('manually', name=f'{Emjois.ICON_NEW} Manually'),
                Choice('config', name=f'{Emjois.ICON_YAML} Yaml configuration')
            ]

            selected_option = prompt_utils.option_select('Network options', choices, separator=True, back=True)

            if selected_option == 'manually':
                self.__create_volume()
            elif selected_option == 'config':
                read_yaml('volumes', self._create_volumes)

    def __create_volume(self):
        volume_name = prompt_utils.text('Volume name', mandatory=False, skip=True)
        if volume_name:
            volume_driver = prompt_utils.text('Volume driver', mandatory=False, skip=True)
            if volume_driver is not None:
                try:
                    self.client.volumes.create(name=volume_name, driver=volume_driver)
                    prompt_utils.success_message(f'Volume {volume_name} created successfully')
                except docker.errors.APIError as e:
                    prompt_utils.error_message(str(e))

    def __get_volumes(self):
        volumes = []
        volume_list = self.client.volumes.list()

        for volume in volume_list:
            volumes.append(Choice(volume.id, name=f'{Emjois.ICON_FLOPPY_DISK} {volume.name}'))

        volumes.sort(key=lambda choice: choice.name)
        return volumes
