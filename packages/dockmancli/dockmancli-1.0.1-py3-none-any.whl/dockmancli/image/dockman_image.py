#!/usr/bin/env python3
import math
import os
from typing import Union

import docker
from InquirerPy.base import Choice
from InquirerPy.separator import Separator
from prompt_toolkit.completion import FuzzyCompleter

from dockmancli.utils import prompt_utils
from dockmancli.utils.spinner import Spinner
from dockmancli.utils import docker_utils
from dockmancli.utils.emjois import Emjois
from dockmancli.utils.dockman_common import read_yaml
from dockmancli.dockman_docker.docker_common import DockerCommon


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


class DockManImage(DockerCommon):

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

            selected_option = prompt_utils.option_select('Image options:', choices)

            if selected_option == 'list':
                self.__list()
            elif selected_option == 'create':
                self.__create()

    def __list(self):
        selected_option = None
        order_desc = False
        autocompleter = False

        while selected_option != prompt_utils.MENU_OPTION_BACK:
            images = docker_utils.get_images(reverse=order_desc, emjoi=not autocompleter)

            choices = images.copy()

            if autocompleter:
                image_names = []
                for choice in choices:
                    image_names.append(choice.name)

                selected_option = prompt_utils.text('Type to select a image', mandatory=False, skip=True,
                                                    completer=FuzzyCompleter(DockerCommon.DockmanCompleter(image_names)),
                                                    validate=lambda result: len(result) > 1,
                                                    invalid_message='Select a valid image')

                if selected_option:
                    image_choice = [x for x in images if x.name == selected_option]
                    if image_choice:
                        selected_option = image_choice[0].value
                    else:
                        prompt_utils.error_message(f'Image "{selected_option}" not found')
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

                selected_option = prompt_utils.option_select('Select image', choices)

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
                    self.__image_options(selected_option)

    def __create(self):
        selected_option = None
        while selected_option != prompt_utils.MENU_OPTION_BACK:
            choices = [
                Choice('pull', name=f'{Emjois.ICON_PULL} Pull'),
                Choice('dockerfile', name=f'{Emjois.ICON_DOCKERFILE} Dockerfile'),
                Choice('config', name=f'{Emjois.ICON_YAML} Yaml configuration')
            ]

            selected_option = prompt_utils.option_select('Image options', choices, separator=True, back=True)

            try:
                if selected_option == 'pull':
                    self.__pull()
                elif selected_option == 'dockerfile':
                    self.__dockerfile()
                elif selected_option == 'config':
                    read_yaml('images', self._create_images)
            except docker.errors.APIError as e:
                prompt_utils.error_message(str(e))

    def __multiselect(self, reverse=False):
        selected_images = None
        while selected_images != prompt_utils.MENU_OPTION_BACK:
            images = docker_utils.get_images(reverse=reverse)
            selected_images = prompt_utils.checkbox('Select images and press Enter', images, mandatory=False)
            if selected_images != prompt_utils.MENU_OPTION_BACK:
                self.__image_options(selected_images)

    def __image_options(self, image_id: Union[str, list[str]]):
        images_ids = []
        choices = [
            Choice('size', name=f'{Emjois.ICON_SIZE} Size'),
            Choice('remove', name=f'{Emjois.ICON_REMOVE} Remove')
        ]
        if isinstance(image_id, str):
            images_ids.append(image_id)
        else:
            images_ids = image_id

        action = prompt_utils.option_select(f'Image options', choices)
        if action == 'remove':
            yes = prompt_utils.confirm_choices()

        for iid in images_ids:
            try:
                if action == 'size':
                    self.__image_size(iid)
                elif action == 'remove':
                    if yes:
                        self.__remove(iid)
            except docker.errors.APIError as e:
                prompt_utils.error_message(str(e))

    def __image_size(self, iid):
        image = self.client.images.get(iid)
        image_name = '<none>:<none>' if len(image.tags) == 0 else image.tags[0]
        size_bytes = image.attrs['Size']
        size = convert_size(size_bytes)
        prompt_utils.info_message(f'Size of image {image_name}: {size}')

    def __remove(self, image_id: str, force=False):
        try:
            image = self.client.images.get(image_id)
            image.remove(force=force)
            image_name = '<none>:<none>' if len(image.tags) == 0 else image.tags[0]
            prompt_utils.success_message(f'Image "{image_name}" removed')
        except docker.errors.APIError as e:
            prompt_utils.error_message(str(e))
            yes = prompt_utils.confirm_choices('Error removing image. Force?')
            if yes:
                try:
                    self.__remove(image_id, force=True)
                except docker.errors.APIError as e:
                    prompt_utils.error_message(str(e))

    def __pull(self):
        pull_image = prompt_utils.text('Enter image name to be pulled', mandatory=False, skip=True)
        if pull_image:
            image = self.client.images.pull(pull_image)
            prompt_utils.success_message(f'Image "{image.tags}" pulled')

    def __dockerfile(self):
        home_path = os.path.expanduser('~')
        dockerfile_path = prompt_utils.filepath('Select Dockerfile', mandatory=False, default_path=home_path)
        if dockerfile_path:
            tag = prompt_utils.text('Enter tag')
            path, dockerfile = os.path.split(dockerfile_path)
            with Spinner(f'{Emjois.ICON_POPCORN} Building image '):
                image, build_logs = self.client.images.build(
                    path=path,
                    dockerfile=dockerfile,
                    tag=tag,
                    forcerm=True)

            prompt_utils.success_message(f'Image "{image.tags[0]}" created')
