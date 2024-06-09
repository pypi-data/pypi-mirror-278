import sys
import time
import threading

from .prompt_utils import COLOR_INFO
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
from prompt_toolkit import print_formatted_text


class Spinner:
    busy = False
    delay = 0.1
    message = None

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\':
                yield cursor

    def __init__(self, message=None, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay):
            self.delay = delay
        if message:
            self.message = message

    def spinner_task(self):
        style = Style.from_dict({'info': COLOR_INFO})

        if self.message:
            text = FormattedText([('class:info', self.message)])
            print_formatted_text(text, style=style, flush=True, end='')

        while self.busy:
            print_formatted_text(FormattedText([('class:info', next(self.spinner_generator))]),
                                 style=style, flush=True, end='')
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

        if self.message:
            sys.stdout.write('\b' * len(self.message))
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            sys.stdout.write('\n')
            return False
