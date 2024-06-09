#!/usr/bin/env python3
import docker
import importlib.metadata

from dockmancli.utils import prompt_utils
from dockmancli.utils.emjois import Emjois
from dockmancli.container.dockman_container import DockManContainer
from dockmancli.network.dockman_network import DockManNetwork
from dockmancli.image.dockman_image import DockManImage
from dockmancli.volume.dockman_volume import DockManVolume
from dockmancli.configuration.dockman_configuration import Configuration

from InquirerPy.base import Choice


def main():
    __show_version()

    option = None
    __check_docker()

    try:
        while option != prompt_utils.MENU_OPTION_EXIT:
            choices = [
                Choice('containers', name=f'{Emjois.ICON_SHIP} Containers'),
                Choice('images', name=f'{Emjois.ICON_DISC} Images'),
                Choice('volumes', name=f'{Emjois.ICON_FLOPPY_DISK} Volumes'),
                Choice('networks', name=f'{Emjois.ICON_NETWORK} Networks'),
                Choice('config', name=f'{Emjois.ICON_YAML} Yaml configuration')
            ]
            option = prompt_utils.option_select('Select an option:', choices=choices, back=False, exit=True,
                                                return_key=False)

            if option == 'containers':
                DockManContainer().main_options()
            elif option == 'images':
                DockManImage().main_options()
            elif option == 'volumes':
                DockManVolume().main_options()
            elif option == 'networks':
                DockManNetwork().main_options()
            elif option == 'config':
                Configuration().main_options()
    except KeyboardInterrupt:
        print('Bye')


def __show_version():
    version = importlib.metadata.version('dockmancli')
    prompt_utils.readonly_message(f'Dockman CLI {version}')


def __check_docker():
    try:
        docker.from_env()
    except:
        raise Exception('Docker not found in the environment')


if __name__ == '__main__':
    main()
