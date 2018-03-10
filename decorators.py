import threading

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
