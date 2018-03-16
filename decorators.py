import threading

from utils.io import log, Color

"""
Set of decorators that can be useful.
"""


def in_thread(method):
    """
    Runs decorated method in a separate, daemon thread.
    :param method:
    :return:
    """

    def run_thread(*args, **kwargs):
        thread = threading.Thread(target=method, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread

    return run_thread


def with_open(filename, mode, exceptions=(IOError,)):
    """
    Runs provided method with additional named parameter being the requested, opened file object,
    located in wrh operating path.
    The additional parameter is available under '_file_' name.
    By default, if the requested file does not exist, method is not invoked but no error is thrown. This can be changed
    by changing exceptions parameter list.
    :param filename: name of the file in the system (wrh operation path is added automatically)
    :type filename: str
    :param mode: mode in which file should be opened
    :type mode: str
    :param exceptions: iterable of exceptions that should be treated as "expected"
    :type exceptions: iterable
    """

    def inner(method):

        def open_and_run(*args, **kwargs):
            try:
                with open(filename, mode) as f:
                    kwargs['_file_'] = f
                    return method(*args, **kwargs)
            except exceptions:
                pass

        return open_and_run

    return inner


def ignore_exceptions(exceptions_list):
    """
    Function wrapper that ignores provided exceptions raised withing wrapped function.
    :param exceptions_list: list of expected exceptions
    """

    def inner(method):
        def run(*args, **kwargs):
            try:
                method(*args, **kwargs)
            except exceptions_list:
                pass

        return run

    return inner


def log_exceptions(exceptions_list=(Exception,)):
    """
    Function wrapper that logs only provided exceptions raised withing wrapped function.
    :param exceptions_list: list of expected exceptions to be logged
    """

    def inner(method):
        def run(*args, **kwargs):
            try:
                method(*args, **kwargs)
            except exceptions_list as e:
                log(e, Color.EXCEPTION)

        return run

    return inner
