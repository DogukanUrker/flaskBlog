# Import the constants module that contains constants for the app
from constants import REGISTRATION  # A constant that apps are allowed to user register


# Define a function that returns a dictionary with the registration enabled
def isRegistration():
    """
    Returns a dictionary with a constant registration is enabled or not.

    Returns:
        dict: A dictionary with a constant registration is enabled or not.
    """

    return dict(isRegistration=REGISTRATION)  # Return the dictionary
