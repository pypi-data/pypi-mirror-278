#!/usr/bin/env python3

from InquirerPy import inquirer
from InquirerPy.base import Choice
from InquirerPy.separator import Separator
from InquirerPy.utils import color_print
from InquirerPy.validator import PathValidator
from dockmancli.utils.emjois import Emjois

COLOR_INFO = '#4083F1'
COLOR_SUCCESS = '#00AD05'
COLOR_ERROR = '#FF0000'
COLOR_GRAY = '#818181'

MENU_OPTION_BACK = 'back'
MENU_OPTION_EXIT = 'exit'


def option_select(message: str, choices: list, mandatory=True, separator=True, back=True, exit=False, style=None, return_key=True):
    options = choices
    if separator:
        options.append(Separator())

    if back:
        options.append(Choice(MENU_OPTION_BACK, name=f'{Emjois.ICON_BACK} Return'))

    if exit:
        options.append(Choice(MENU_OPTION_EXIT, name=f'{Emjois.ICON_EXIT} Exit'))

    if return_key:
        prompt = inquirer.select(
            message=message,
            choices=options,
            mandatory=mandatory,
            style=style
        )

        @prompt.register_kb('escape')
        def _handle_return(event):
            event.app.exit(result=MENU_OPTION_BACK)

        option = prompt.execute()
    else:
        option = inquirer.select(
            message=message,
            choices=options,
            mandatory=mandatory,
            style=style
        ).execute()

    return option


def text(message: str, mandatory=True, skip=False, keybindings=None, style=None, completer=None, transformer=None,
         filter=None, validate=None, invalid_message='Invalid input'):
    if skip:
        keybindings = __add_skip_keybinding(keybindings)
        message = message + '. Press escape to cancel'

    response = inquirer.text(
        message=message,
        mandatory=mandatory,
        keybindings=keybindings,
        style=style,
        completer=completer,
        transformer=transformer,
        filter=filter,
        validate=validate,
        invalid_message=invalid_message
    ).execute()

    return response


def filepath(message: str, mandatory=True, default_path='', keybindings=None):
    if not mandatory:
        keybindings = __add_skip_keybinding(keybindings)
        message = message + '. Press escape to cancel'

    selected_path = inquirer.filepath(
        message=message,
        default=default_path,
        validate=PathValidator(is_file=True, message='Input is not a file'),
        mandatory=mandatory,
        keybindings=keybindings
    ).execute()

    return selected_path


def checkbox(message: str, choices: list, cycle=True, mandatory=True, style=None, transformer=None, return_key=True):
    if return_key:
        message = message + '. Press escape to cancel'

    if return_key:
        prompt = inquirer.checkbox(
            message=message,
            choices=choices,
            mandatory=mandatory,
            cycle=cycle,
            style=style,
            transformer=transformer
        )

        @prompt.register_kb('escape')
        def _handle_return(event):
            event.app.exit(result=MENU_OPTION_BACK)

        selected_options = prompt.execute()
    else:
        selected_options = inquirer.checkbox(
            message=message,
            choices=choices,
            mandatory=mandatory,
            cycle=cycle,
            style=style,
            transformer=transformer
        ).execute()

    return selected_options


def confirm_choices(message='Are you sure?') -> any:
    return inquirer.confirm(message).execute()


def success_message(message: str):
    color_print(formatted_text=[('class:success', f'{Emjois.ICON_FINGER_UP} {message}')],
                style={'success': COLOR_SUCCESS})


def info_message(message: str):
    color_print(formatted_text=[('class:info', f'{Emjois.ICON_FINGER_POINTING_RIGHT} {message}')],
                style={'info': COLOR_INFO})


def error_message(message: str):
    color_print(formatted_text=[('class:error', f'{Emjois.ICON_FINGER_DOWN} {message}')], style={'error': COLOR_ERROR})


def readonly_message(message: str):
    color_print(formatted_text=[('class:error', message)], style={'error': COLOR_GRAY})


def print_default(message: str):
    print(message)


def __add_skip_keybinding(keybindings=None):
    if keybindings:
        keybindings['skip'] = [{'key': 'escape'}]
    else:
        keybindings = {
            'skip': [{'key': 'escape'}]
        }

    return keybindings
