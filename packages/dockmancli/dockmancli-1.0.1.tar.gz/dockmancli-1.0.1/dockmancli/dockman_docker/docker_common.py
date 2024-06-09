#!/usr/bin/env python3

import docker
from prompt_toolkit.completion import Completer, Completion

from dockmancli.utils import prompt_utils
from dockmancli.utils import docker_utils
from dockmancli.utils.emjois import Emjois
from dockmancli.utils.spinner import Spinner


class DockerCommon:

    def __init__(self):
        self.client = docker.from_env()

    class DockmanCompleter(Completer):

        def __init__(self, choices: [str]):
            self._choices = choices

        def get_completions(self, document, complete_event):
            for choice in self._choices:
                yield Completion(
                    choice,
                    style='bg:lightblue fg:ansiblack'
                )

    def _create_images(self, images: dict):
        for image in images:
            if 'image' in image:
                if 'tag' in image['image']:
                    image_tag = image['image']['tag']
                    try:
                        with Spinner(f'{Emjois.ICON_POPCORN} Building image {image_tag} '):
                            for conf in image:
                                values = image[conf]

                            image, build_logs = self.client.images.build(**values)

                        prompt_utils.success_message(f'Image "{image.tags[0]}" created')
                    except docker.errors.BuildError as e:
                        for line in e.build_log:
                            if 'stream' in line:
                                prompt_utils.print_default(line['stream'].strip())
                        error_message = f'Error creating image "{image_tag}": {str(e)}'
                        prompt_utils.error_message(error_message)
                else:
                    prompt_utils.error_message('Image has not "tag" key')
            else:
                prompt_utils.error_message('Yaml has not "image" key')

    def _create_containers(self, containers: dict):
        for idx, container in enumerate(containers):
            try:
                if 'image' in container['container']:
                    image = container['container']['image']
                    del container['container']['image']
                    self.__create_container(container, image)
                else:
                    yes = prompt_utils.confirm_choices(f'No image provided for containers.container[{idx}]. Do you want select one?')
                    if yes:
                        images = docker_utils.get_images()
                        selected_image_id = prompt_utils.option_select('Select image', images)

                        if selected_image_id != prompt_utils.MENU_OPTION_BACK:
                            image = self.client.images.get(selected_image_id)
                            self.__create_container(container, image)
                    else:
                        prompt_utils.info_message('No image selected. Container cannot be created')
            except docker.errors.APIError as e:
                prompt_utils.error_message(str(e))

    def _create_networks(self, networks: dict):
        for idx, network in enumerate(networks):
            try:
                if 'network' in network:
                    for conf in network:
                        values = network[conf]

                    network_created = self.client.networks.create(**values)
                    prompt_utils.success_message(f'Network {network_created.name} created successfully')
                else:
                    prompt_utils.error_message('Yaml has not "network" key')
            except docker.errors.APIError as e:
                prompt_utils.error_message(str(e))

    def _create_volumes(self, volumes: dict):
        for idx, volume in enumerate(volumes):
            try:
                if 'volume' in volume:
                    for conf in volume:
                        values = volume[conf]

                    volume_created = self.client.volumes.create(**values)
                    prompt_utils.success_message(f'Volume {volume_created.name} created successfully')
                else:
                    prompt_utils.error_message('Yaml has not "volume" key')
            except docker.errors.APIError as e:
                prompt_utils.error_message(str(e))

    def __create_container(self, container, image):
        for conf in container:
            values = container[conf]
            container = self.client.containers.create(image, command=None, **values)

            prompt_utils.success_message(f'Container "{container.name}" created successfully')
