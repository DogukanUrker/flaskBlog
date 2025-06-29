# Import the constants module that contains constants for the app
from constants import LOG_IN  # A constant that apps are allowed to user login


# Define a function that returns a dictionary with the login enabled
def isLogin():
    """
    Returns a dictionary with a constant login is enabled or not.

    Returns:
        dict: A dictionary with a constant login is enabled or not.
    """

    return dict(isLogin=LOG_IN)  # Return the dictionary
