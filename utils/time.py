"""
Importing necessary modules.
"""

from modules import tzname, datetime


# Function to get the current system time zone
def currentTimeZone():
    """
    Returns the current system time zone as a string.
    """
    return tzname[
        0
    ]  # Return the first element of the tzname list, which typically represents the time zone name.


# Function to get the current date in the format "dd.mm.yy"
def currentDate():
    """
    Returns the current date as a string in the format "dd.mm.yy".
    """
    return datetime.now().strftime(
        "%d.%m.%y"
    )  # Return current date formatted as day.month.year.


# Function to get the current time
def currentTime(seconds=False, microSeconds=False):
    """
    Returns the current time as a string in the format "HH:MM" or "HH:MM:SS" depending on the value of the seconds parameter. If the microSeconds parameter is set to True, the time will include microseconds as well.
    """
    match seconds:  # Using pattern matching to handle different cases
        case False:
            return datetime.now().strftime(
                "%H:%M"
            )  # Return current time formatted as hour:minute.
        case True:
            match microSeconds:  # Nested pattern matching to handle microseconds
                case True:
                    return datetime.now().strftime(
                        "%H:%M:%S.%f"
                    )  # Return current time with microseconds.
                case False:
                    return datetime.now().strftime(
                        "%H:%M:%S"
                    )  # Return current time with seconds.


# Function to get the current timestamp
def currentTimeStamp():
    """
    Returns the current time stamp as an integer.
    """
    timeStamp = (
        datetime.now().timestamp()
    )  # Get current timestamp using datetime module.
    timeStamp = int(timeStamp)  # Convert timestamp to integer.
    return timeStamp  # Return the integer timestamp.
