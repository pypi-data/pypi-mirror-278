#!/usr/bin/env python3
from typing import Union

import docker
from InquirerPy.base import Choice
from InquirerPy.separator import Separator
from docker.models.containers import Container
from docker.models.networks import Network
from prompt_toolkit.completion import FuzzyCompleter

from dockmancli.utils import prompt_utils
from dockmancli.utils import docker_utils
from dockmancli.utils.emjois import Emjois
from dockmancli.utils.dockman_common import read_yaml
from dockmancli.dockman_docker.docker_common import DockerCommon


class DockManNetwork(DockerCommon):

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

            selected_option = prompt_utils.option_select('Network options:', choices)

            if selected_option == 'list':
                self.__list()
            elif selected_option == 'create':
                self.__create()

    def __list(self):
        selected_option = None
        order_desc = False
        autocompleter = False

        while selected_option != prompt_utils.MENU_OPTION_BACK:
            networks = docker_utils.get_networks(reverse=order_desc, emjoi=not autocompleter)

            choices = networks.copy()

            if autocompleter:
                network_names = []
                for choice in choices:
                    network_names.append(choice.name)

                selected_option = prompt_utils.text('Type to select a network', mandatory=False, skip=True,
                                                    completer=FuzzyCompleter(DockerCommon.DockmanCompleter(network_names)),
                                                    validate=lambda result: len(result) > 1,
                                                    invalid_message='Select a valid network')

                if selected_option:
                    image_choice = [x for x in networks if x.name == selected_option]
                    if image_choice:
                        selected_option = image_choice[0].value
                    else:
                        prompt_utils.error_message(f'Networks "{selected_option}" not found')
                        selected_option = None
                else:
                    autocompleter = False
            else:
                choices.append(Separator())
                choices.append(Choice('multiselect', name=f'{Emjois.ICON_CHECK} Multiselect'))
                choices.append(Choice('autocompleter', name=f'{Emjois.ICON_AUTOCOMPLETE} Autocompleter'))

                if order_desc:
                    choices.append(Choice('order_asc', name=f'{Emjois.ICON_ARROW_UP} Order asc'))
                else:
                    choices.append(Choice('order_desc', name=f'{Emjois.ICON_ARROW_DOWN} Order desc'))

                selected_option = prompt_utils.option_select('Select network', choices)

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
                else:
                    self.__network_options(selected_option)

    def __multiselect(self, reverse=False):
        selected_networks = None
        while selected_networks != prompt_utils.MENU_OPTION_BACK:
            networks = docker_utils.get_networks(reverse=reverse)
            selected_networks = prompt_utils.checkbox('Select networks and press Enter', networks, mandatory=False)
            if selected_networks != prompt_utils.MENU_OPTION_BACK:
                self.__network_options(selected_networks)

    def __network_options(self, network_id: Union[str, list[str]]):
        networks_ids = []
        choices = []

        if isinstance(network_id, str):
            networks_ids.append(network_id)
            choices = [
                Choice('containers', name=f'{Emjois.ICON_NETWORK} Connected containers (must be started)'),
                Choice('connect', name=f'{Emjois.ICON_NETWORK} Connect to container')
            ]
        else:
            networks_ids = network_id

        choices.append(Choice('remove', name=f'{Emjois.ICON_REMOVE} Remove'))

        action = prompt_utils.option_select(f'Network options', choices)
        if action == 'remove':
            yes = prompt_utils.confirm_choices()

        for nid in networks_ids:
            try:
                if action == 'containers':
                    self.__connected_containers(nid)
                elif action == 'connect':
                    self.__connect(nid)
                elif action == 'remove':
                    if yes:
                        self.__remove(nid)
            except docker.errors.APIError as e:
                prompt_utils.error_message(str(e))

    def __connected_containers(self, network_id):
        network = self.client.networks.get(network_id)
        container_list = network.containers
        containers = []

        for container in container_list:
            containers.append(Choice(container.id, name=container.name))

        selected_container_id = prompt_utils.option_select('Connected containers', containers)
        if selected_container_id != prompt_utils.MENU_OPTION_BACK:
            container = next((x for x in container_list if x.id == selected_container_id), None)
            choices = [
                Choice('disconnect', name='Disconnect'),
                Choice('reload', name='Reload')
            ]
            selected_option = prompt_utils.option_select('Container network options', choices)

            if selected_option == 'disconnect':
                self.__disconnect(network, container)
            elif selected_option == 'reload':
                self.__reload(network)

    def __connect(self, network_id):
        containers = docker_utils.get_containers()

        selected_option = prompt_utils.option_select('Select container', containers)
        if selected_option != prompt_utils.MENU_OPTION_BACK:
            container = next((x for x in containers if x.value == selected_option), None)
            network = self.client.networks.get(network_id)

            network.connect(selected_option)
            prompt_utils.success_message(f'Network "{network.name}" connected to container "{container.name}"')

    def __disconnect(self, network: Network, container: Container):
        yes = prompt_utils.confirm_choices(f'Disconnect network "{network.name}" from the container "{container.name}"?')

        if yes:
            try:
                network.disconnect(container)
                prompt_utils.success_message(f'Network "{network.name}" disconnected from container "{container.name}"')
            except docker.errors.APIError as e:
                prompt_utils.error_message(str(e))

    def __reload(self, network: Network):
        try:
            network.reload()
            prompt_utils.success_message(f'Network "{network.name}" reloaded')
        except docker.errors.APIError as e:
            prompt_utils.error_message(str(e))

    def __remove(self, network_id):
        try:
            network = self.client.networks.get(network_id)
            network.remove()
            prompt_utils.success_message(f'Network "{network.name}" removed')
        except docker.errors.APIError as e:
            prompt_utils.error_message(str(e))

    def __create(self):
        selected_option = None
        while selected_option != prompt_utils.MENU_OPTION_BACK:
            choices = [
                Choice('manually', name=f'{Emjois.ICON_NEW} Manually'),
                Choice('config', name=f'{Emjois.ICON_YAML} Yaml configuration')
            ]

            selected_option = prompt_utils.option_select('Network options', choices, separator=True, back=True)

            if selected_option == 'manually':
                self.__create_network()
            elif selected_option == 'config':
                read_yaml('networks', self._create_networks)

    def __create_network(self):
        network_name = prompt_utils.text('Network name', mandatory=False, skip=True,
                                         validate=lambda result: len(result) > 1, invalid_message='Enter a valid name')
        if network_name:
            network_driver = prompt_utils.text('Network driver', mandatory=False, skip=True,
                                               validate=lambda result: len(result) > 1,
                                               invalid_message='Enter a valid driver')
            if network_driver:
                try:
                    self.client.networks.create(network_name, driver=network_driver)
                    prompt_utils.success_message(f'Network {network_name} created successfully')
                except docker.errors.APIError as e:
                    prompt_utils.error_message(str(e))
