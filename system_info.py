"""
Set of instructions for getting information about the system.
"""

from urllib.error import URLError
from urllib.request import urlopen


def get_cpu_temp():
    """
    Returns information about cpu temperature.
    :return: cpu temperature float value
    """
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as temp_file:
            cpu_temp = float(temp_file.read()) / 1000
    except (FileNotFoundError, ValueError):
        cpu_temp = '?'
    return cpu_temp


def get_uptime():
    """
    Returns pretty string about system uptime.
    :return: uptime string
    """
    uptime_string = ""

    with open('/proc/uptime', 'r') as f:
        total_seconds = float(f.readline().split()[0])

        # Helper vars:
        minute = 60
        hour = minute * 60
        day = hour * 24

        # Get the days, hours, etc:
        days = int(total_seconds / day)
        hours = int((total_seconds % day) / hour)
        minutes = int((total_seconds % hour) / minute)
        seconds = int(total_seconds % minute)

        # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
        if days > 0:
            uptime_string += str(days) + " " + (days == 1 and "day" or "days") + ", "
        if len(uptime_string) > 0 or hours > 0:
            uptime_string += str(hours) + " " + (hours == 1 and "hour" or "hours") + ", "
        if len(uptime_string) > 0 or minutes > 0:
            uptime_string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes") + ", "
        uptime_string += str(seconds) + " " + (seconds == 1 and "second" or "seconds")
    return uptime_string


def is_internet_connection():
    """
    Checks if Internet connection is present.
    This method uses DNS to determine IP address of https://www.google.com web page.
    Although it's not an optimal way, this function is given as it is.
    :return: boolean information whether Internet connection is present
    """
    try:
        urlopen('https://www.google.com', timeout=5)
        is_internet = True
    except URLError:
        is_internet = False
    return is_internet
