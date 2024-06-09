#!/usr/bin/env python3
import re
from typing import Union

import dateutil.parser as dparser
import docker
from InquirerPy.base import Choice
from InquirerPy.separator import Separator
from prompt_toolkit.completion import FuzzyCompleter

from dockmancli.dockman_docker.docker_common import DockerCommon
from dockmancli.utils import docker_utils
from dockmancli.utils import prompt_utils
from dockmancli.utils.dockman_common import read_yaml
from dockmancli.utils.emjois import Emjois


def _remove_status(result):
    if result:
        containers_status = result
        if isinstance(result, str):
            containers_status = [result]

        container_without_status = []
        for container_name in containers_status:
            match = re.search(' \\(' + docker_utils.Status.exited.value + '\\)|' +
                              ' \\(' + docker_utils.Status.running.value + '\\)|' +
                              ' \\(' + docker_utils.Status.created.value + '\\)|' +
                              ' \\(' + docker_utils.Status.stopped.value + '\\) ',
                              container_name)

            if match:
                container_without_status.append(container_name.replace(match.group(0), ''))

        if container_without_status:
            container_without_status = container_without_status if isinstance(result, list) else container_without_status[0]
        else:
            container_without_status = result
        return container_without_status


class DockManContainer(DockerCommon):

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

            selected_option = prompt_utils.option_select('Container options:', choices)

            if selected_option == 'list':
                self.__list()
            elif selected_option == 'create':
                self.__create()

    def __list(self):
        selected_option = None
        order_desc = False
        autocompleter = False

        while selected_option != prompt_utils.MENU_OPTION_BACK:
            containers = docker_utils.get_containers(reverse=order_desc, emjoi=not autocompleter)

            choices = containers.copy()

            if autocompleter:
                container_names = []
                for choice in choices:
                    container_names.append(choice.name)

                selected_option = prompt_utils.text(
                    'Type to select a container', mandatory=False, skip=True,
                    completer=FuzzyCompleter(DockerCommon.DockmanCompleter(container_names)),
                    filter=_remove_status, transformer=_remove_status, validate=lambda result: len(result) > 1,
                    invalid_message='Select a valid container')

                if selected_option:
                    container_choice = [x for x in containers if _remove_status(x.name) == selected_option]
                    if container_choice:
                        selected_option = container_choice[0].value
                    else:
                        prompt_utils.error_message(f'Container "{selected_option}" not found')
                        selected_option = None
                else:
                    autocompleter = False
            else:
                choices.append(Separator())
                choices.append(Choice('multiselect', name=f'{Emjois.ICON_CHECK} Multiselect'))
                choices.append(Choice('autocompleter', name=f'{Emjois.ICON_AUTOCOMPLETE} Autocompleter'))
                choices.append(Choice('refresh', name=f'{Emjois.ICON_REFRESH} Refresh'))

                if order_desc:
                    choices.append(Choice('order_asc', name=f'{Emjois.ICON_ARROW_UP} Order asc'))
                else:
                    choices.append(Choice('order_desc', name=f'{Emjois.ICON_ARROW_DOWN} Order desc'))

                selected_option = prompt_utils.option_select('Select container', choices)

            if selected_option and selected_option != prompt_utils.MENU_OPTION_BACK:
                if selected_option == 'multiselect':
                    self.__multiselect(reverse=order_desc)
                elif selected_option == 'autocompleter':
                    autocompleter = True
                elif 'order' in selected_option:
                    if 'asc' in selected_option:
                        order_desc = False
                    else:
                        order_desc = True
                elif selected_option != 'refresh':
                    self.__container_options(selected_option)

    def __create(self):
        choices = [
            Choice('image', name=f'{Emjois.ICON_DISC} Image'),
            Choice('config', name=f'{Emjois.ICON_YAML} Yaml configuration')
        ]

        selected_option = prompt_utils.option_select('Create container with basic options', choices,
                                                     separator=True, back=True)

        if selected_option == 'config':
            read_yaml('containers', self._create_containers)
        elif selected_option == 'image':
            self.__create_from_image()

    def __multiselect(self, reverse=False):
        selected_containers = None
        while selected_containers != prompt_utils.MENU_OPTION_BACK:
            containers = docker_utils.get_containers(reverse=reverse)
            selected_containers = prompt_utils.checkbox('Select containers and press Enter', containers,
                                                        mandatory=False, transformer=_remove_status)
            if selected_containers != prompt_utils.MENU_OPTION_BACK:
                self.__container_options(selected_containers)

    def __container_options(self, container_id: Union[str, list[str]]):
        choices = []
        containers_ids = []
        if isinstance(container_id, str):
            status = docker_utils.container_status(container_id)

            if status == docker_utils.Status.running:
                choices.append(Choice('stop', name=f'{Emjois.ICON_STOP} Stop'))
            elif (status == docker_utils.Status.stopped or status == docker_utils.Status.exited or
                  status == docker_utils.Status.created):
                choices.append(Choice('start', name=f'{Emjois.ICON_START} Start'))
            choices.append(Choice('rename', name=f'{Emjois.ICON_RENAME} Rename'))
            choices.append(Choice('logs', name=f'{Emjois.ICON_LOGS} Logs'))

            container_name = docker_utils.get_container_name(container_id)
            message = f'Container "{container_name}" is {status.value}'
            containers_ids.append(container_id)
        else:
            choices.append(Choice('start', name=f'{Emjois.ICON_START} Start'))
            choices.append(Choice('stop', name=f'{Emjois.ICON_STOP} Stop'))
            message = 'Select an option for all containers'
            containers_ids = container_id

        choices.append(Choice('restart', name=f'{Emjois.ICON_RESTART} Restart'))
        choices.append(Choice('remove', name=f'{Emjois.ICON_REMOVE} Remove'))

        action = prompt_utils.option_select(message, choices)
        if action == 'remove':
            yes = prompt_utils.confirm_choices()

        for cid in containers_ids:
            try:
                if action == 'start':
                    self.__start(cid)
                elif action == 'stop':
                    self.__stop(cid)
                elif action == 'restart':
                    self.__restart(cid)
                elif action == 'remove':
                    if yes:
                        self.__remove(cid)
                elif action == 'rename':
                    self.__rename(cid)
                elif action == 'logs':
                    self.__logs_options(cid)
            except docker.errors.APIError as e:
                prompt_utils.error_message(str(e))

    def __start(self, container_id: str):
        container = self.client.containers.get(container_id)
        prompt_utils.info_message(f'Starting container "{container.name}"')
        container.start()

    def __stop(self, container_id: str):
        container = self.client.containers.get(container_id)
        prompt_utils.info_message(f'Stopping container "{container.name}"')
        container.stop()

    def __restart(self, container_id: str):
        container = self.client.containers.get(container_id)
        prompt_utils.info_message(f'Restarting container "{container.name}"')
        container.restart()

    def __remove(self, container_id: str):
        container = self.client.containers.get(container_id)
        status = docker_utils.container_status(container_id)

        if status == docker_utils.Status.running:
            self.__stop(container_id)
        container.remove()
        prompt_utils.info_message(f'Removed container "{container.name}"')

    def __rename(self, container_id: str):
        container_name = self.__get_container_name(container_id)
        message = f'Enter new container name for "{container_name}"'
        new_name = prompt_utils.text(message, mandatory=False, skip=True)

        if new_name:
            prompt_utils.info_message(f'Container renamed to "{new_name}"')
            container = self.client.containers.get(container_id)
            container.rename(new_name)

    def __logs_options(self, container_id: str):
        selected_option = None

        while selected_option != prompt_utils.MENU_OPTION_BACK:
            choices = [
                Choice('all', name=f'{Emjois.ICON_LOGS} Show all'),
                Choice('follow', name=f'{Emjois.ICON_LOGS} Follow (Press Control + c to exit)')
            ]

            selected_option = prompt_utils.option_select('Select a log option:', choices=choices)

            if selected_option and selected_option != prompt_utils.MENU_OPTION_BACK:
                if selected_option == 'all':
                    self.__logs_all(container_id)
                elif selected_option == 'follow':
                    self.__logs_follow(container_id)

    def __logs_all(self, container_id: str):
        container = self.client.containers.get(container_id)
        container_logs = container.logs()
        prompt_utils.print_default(container_logs.decode("utf-8"))

    def __logs_follow(self, container_id: str):
        container = self.client.containers.get(container_id)
        since = None
        try:
            last_timestamp = None
            while True:
                container_logs = container.logs(stream=True, follow=False, timestamps=True, since=since)
                for bytes_log in container_logs:
                    log = bytes_log.decode("utf-8")
                    last_timestamp = re.search('\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{9}Z ', log).group(0)
                    prompt_utils.print_default(log.replace('\n', ' ').replace(last_timestamp, ''))

                since = dparser.parse(last_timestamp, fuzzy=True).timestamp()
                since = int(since) + float(re.search('.\d{9}', last_timestamp.strip()).group(0)) + 0.000001
        except KeyboardInterrupt:
            pass

    def __get_container_name(self, container_id: str) -> str:
        container = self.client.containers.get(container_id)
        return container.name

    def __create_from_image(self):
        images = docker_utils.get_images()

        selected_image_id = prompt_utils.option_select('Select image', images)
        if selected_image_id and selected_image_id != prompt_utils.MENU_OPTION_BACK:
            ports = prompt_utils.text('Set host_port:container_port', mandatory=False, skip=True)
            if ports and ports != prompt_utils.MENU_OPTION_BACK:
                memory = prompt_utils.text('Set memory (100m, 1g)', mandatory=False, skip=True)
                if memory and memory != prompt_utils.MENU_OPTION_BACK:
                    container_name = prompt_utils.text('Container name', mandatory=False, skip=True,
                                                       validate=lambda result: len(result) > 1,
                                                       invalid_message='Enter a container name')
                    if container_name and container_name != prompt_utils.MENU_OPTION_BACK:
                        mapped_ports = {}
                        if ports:
                            host_port, container_port = ports.split(':')
                            mapped_ports = {container_port: host_port}

                        image = self.client.images.get(selected_image_id)

                        self.client.containers.create(
                            image,
                            mem_limit=memory,
                            ports=mapped_ports,
                            name=container_name
                        )

                        prompt_utils.success_message(f'Container "{container_name}" created')
