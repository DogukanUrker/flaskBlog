from modules import tzname, datetime


# Function to get the current system time zone
def currentTimeZone():
    """
    Returns the current system time zone as a string.
    """
    return tzname[0]


# Function to get the current date in the format "dd.mm.yy"
def currentDate():
    """
    Returns the current date as a string in the format "dd.mm.yy".
    """
    return datetime.now().strftime("%d.%m.%y")


# Function to get the current time
def currentTime(seconds=False, microSeconds=False):
    """
    Returns the current time as a string in the format "HH:MM" or "HH:MM:SS" depending on the value of the seconds parameter. If the microSeconds parameter is set to True, the time will include microseconds as well.
    """
    match seconds:
        case False:
            return datetime.now().strftime("%H:%M")
        case True:
            match microSeconds:
                case True:
                    return datetime.now().strftime("%H:%M:%S.%f")
                case False:
                    return datetime.now().strftime("%H:%M:%S")


# Function to get the current timestamp
def currentTimeStamp():
    """
    Returns the current time stamp as an integer.
    """
    timeStamp = datetime.now().timestamp()  # Get current timestamp
    timeStamp = int(timeStamp)  # Convert to integer
    return timeStamp
