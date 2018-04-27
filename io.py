import inspect
import logging

import os
from enum import Enum

"""
Set of commands to deal with input/output operations.
"""

logging.basicConfig(filename='/tmp/wrh.log', level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S",
                    format='%(asctime)s %(levelname)s %(message)s')


class Color(Enum):
    NORMAL = '\033[0m'
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    EXCEPTION = str(FAIL) + str(BOLD)

    def __str__(self):
        return str(self.value)


def log(message, color=Color.NORMAL, *colors):
    """
    Prints provided message to the screen using color of choice.
    Messages with Fail or WARNING colors are additionally saved to log file.
    :param message: text to display
    :param color: color enum
    :param colors: any number of additional styles applied to displayed text
    """
    styles = (color, ) + colors
    decoration = ''.join(map(str, styles))
    msg = ''.join((decoration, str(message), str(Color.NORMAL)))
    print(msg)

    caller_info = inspect.getframeinfo(inspect.currentframe().f_back)
    msg = 'in {} line {}: {}'.format(caller_info.filename.split(os.sep)[-1], caller_info.lineno, message)
    if Color.FAIL in styles:
        logging.error(msg)
    elif Color.FAIL in styles:
        logging.error(msg)
    elif Color.EXCEPTION in styles:
        logging.exception(msg)
    else:
        logging.info(msg)


def wrh_input(allowed_empty=False, message='', input_type=str, sanitizer=lambda x: True, allowed_exceptions=()):
    """
    Input sanitizing function that can be used for requesting specific input formats.
    (see non_empty_numeric_input(), etc.)
    :param allowed_empty: is input allowed to be empty
    :param message: message to be displayed
    :param input_type: type of the expected input (str, int, Object())
    :type input_type: any
    :param sanitizer: function returning bool value, that checks if input is OK
    :param allowed_exceptions: exceptions that should not be raised during input parsing
    :return: parsed user's input
    """
    while True:
        try:
            answer = input(message)
            if allowed_empty and not answer:
                break
            answer = input_type(answer)
            if not sanitizer(answer):
                continue
            break
        except allowed_exceptions:
            pass
    return answer


def non_empty_input(message='', **kwargs):
    """
    Reads user input discarding all empty messages.
    :param message: message to display
    :param kwargs: additional kwargs to be passed to wrh_input()
    :return: user's input
    """
    return wrh_input(message=message, **kwargs)


def non_empty_numeric_input(message='', **kwargs):
    """
    Reads user input discarding all empty and non-integer messages
    :param message: message to display
    :param kwargs: additional kwargs to be passed to wrh_input()
    :return: user's input number
    """
    return wrh_input(message=message, input_type=int, allowed_exceptions=(ValueError,), **kwargs)


def non_empty_positive_numeric_input(message='', **kwargs):
    """
    Reads user input discarding all empty and non-integer messages
    :param message: message to display
    :param kwargs: additional kwargs to be passed to wrh_input()
    :return: user's input number
    """
    return wrh_input(message=message, input_type=int, sanitizer=lambda x: x >= 0, allowed_exceptions=(ValueError,),
                     **kwargs)
