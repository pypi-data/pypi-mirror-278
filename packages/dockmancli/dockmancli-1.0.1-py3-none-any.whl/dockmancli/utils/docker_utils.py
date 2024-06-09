#!/usr/bin/env python3
from enum import Enum

import docker
from InquirerPy.base import Choice
from .emjois import Emjois

client = docker.from_env()


class Status(Enum):
    created = 'created'
    stopped = 'stopped'
    running = 'running'
    exited = 'exited'

    @staticmethod
    def from_str(str_status: str):
        if str_status == 'created':
            return Status.created
        elif str_status == 'stopped':
            return Status.stopped
        elif str_status == 'running':
            return Status.running
        elif str_status == 'exited':
            return Status.exited


def get_images(reverse=False, emjoi=True) -> list[Choice]:
    images = []
    image_list = client.images.list()

    for image in image_list:
        image_name = '<none>:<none>' if len(image.tags) == 0 else image.tags[0]

        if emjoi:
            image_name = f'{Emjois.ICON_DISC} {image_name}'
        images.append(Choice(image.id, name=image_name))

    if reverse is not None:
        images.sort(key=lambda choice: choice.name, reverse=reverse)
    return images


def get_containers(all_containers=True, add_status=True, reverse=False, emjoi=True) -> list[Choice]:
    containers = []
    container_list = client.containers.list(all=all_containers)
    for container in container_list:
        if add_status:
            status = container_status(container.id)
            name = f'{container.name} ({status.value})'
        else:
            name = f'{container.name}'

        if emjoi:
            name = f'{Emjois.ICON_SHIP} {name}'

        containers.append(Choice(container.id, name=name))

    if reverse is not None:
        containers.sort(key=lambda choice: choice.name, reverse=reverse)
    return containers


def get_container_name(container_id) -> str:
    container = client.containers.get(container_id)
    return container.name


def get_networks(reverse=False, emjoi=True) -> list[Choice]:
    networks = []
    network_list = client.networks.list()

    for network in network_list:
        if emjoi:
            name = f'{Emjois.ICON_NETWORK} {network.name}'
        else:
            name = network.name

        networks.append(Choice(network.id, name=name))

    if reverse is not None:
        networks.sort(key=lambda choice: choice.name, reverse=reverse)
    return networks


def container_status(container_id: str) -> Status:
    container = client.containers.get(container_id)
    return Status.from_str(container.status)
