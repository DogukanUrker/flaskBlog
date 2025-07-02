"""
This module contains the current time variables.
"""

from datetime import datetime
from time import tzname


def currentTimeZone():
    """
    Returns the current system time zone as a string.
    """
    return tzname[0]


def currentDate():
    """
    Returns the current date as a string in the format "dd.mm.yy".
    """
    return datetime.now().strftime("%d.%m.%y")


def currentTime(seconds=False, microSeconds=False):
    """
    Returns the current time as a string in the format "HH:MM" or "HH:MM:SS" depending on the value of the seconds parameter. If the microSeconds parameter is set to True, the time will include microseconds as well.
    """
    if not seconds:
        return datetime.now().strftime("%H:%M")
    else:
        if microSeconds:
            return datetime.now().strftime("%H:%M:%S.%f")
        else:
            return datetime.now().strftime("%H:%M:%S")


def currentTimeStamp():
    """
    Returns the current time stamp as an integer.
    """
    timeStamp = datetime.now().timestamp()
    timeStamp = int(timeStamp)
    return timeStamp
