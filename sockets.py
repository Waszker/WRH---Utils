import socket as s
import time

from utils.io import log, Color

"""
Set of functions to make socket handling a lot easier.
"""


def wait_bind_socket(socket, host, port, sleep, retries=-1, predicate=lambda: True, error_message=None):
    """
    Tries to bind socket for specified host and port.
    In case of failure the procedure is retried until predicate value is False or provided
    number of retries is achieved. After each failure the procedure sleeps for a sleep number
    of seconds.
    """
    while predicate() and retries != 0:
        try:
            socket.bind((str(host), int(port)))
            break
        except s.error as message:
            if error_message:
                log(str(error_message) + str(message), Color.EXCEPTION)
            time.sleep(sleep)
            retries = max(-1, retries - 1)
    return predicate() and retries != 0


def await_connection(socket, callback, predicate=lambda: True, close_connection=True):
    """
    Waits for connection on provided socket. Each connection results in firing provided
    callback function with the connection and client address as arguments.
    Connection
    """
    while predicate():
        try:
            connection, address = socket.accept()
            callback(connection, address)
            if close_connection:
                connection.close()
        except (s.error, OSError):
            pass


def open_connection(*args, **kwargs):
    """
    Generator method for opening TCP connections.
    """
    connection = None
    try:
        connection = s.create_connection(*args, **kwargs)
        yield connection
    except s.error:
        pass
    finally:
        if connection:
            connection.close()


def receive_message(host, port, buffer_size=1024, message=None):
    """
    Receives message with the maximum size of buffer_size from host on provided port.
    If the optional parameter message is not None then this message is sent prior to receiving procedure.
    This method does not raise exceptions if anything regarding socket connection goes wrong.
    :param host: host to connect to
    :param port: port to connect to
    :param buffer_size: size of the buffer for receiving the message
    :param message: message to send prior to receiving
    :return: received message, None if an error occurred or no message was received
    """
    host, port = str(host), int(port)
    data = None
    for connection in open_connection((host, port)):
        if message:
            connection.send(message)
        data = connection.recv(buffer_size)
    return data


def send_message(host, port, message):
    """
    Sends message to provided host on certain port.
    This method does not raise exceptions if anything regarding socket connection goes wrong.
    :param host: host to connect to
    :param port: port to connect to
    :param message: message to send
    """
    host, port = str(host), int(port)
    for connection in open_connection((host, port)):
        connection.send(message)
