# Import the helpers module that contains constants and functions for the app
from helpers import (
    LOG_IN,  # A constant that apps is allowed to user log in
    RECAPTCHA,  # A constant that indicates if the recaptcha is enabled
    REGISTRATION,  # A constant that apps is allowed to user register
    RECAPTCHA_BADGE,  # A constant indicating whether the recaptcha badge should be visible or not
    getProfilePicture,  # A function that returns the user's profile picture URL
)


# Define a function that returns a dictionary with the user's profile picture URL
def returnUserProfilePicture():
    """
    Returns a dictionary with the user's profile picture URL.

    Returns:
        dict: A dictionary containing the user's profile picture URL.
    """

    return dict(getProfilePicture=getProfilePicture)  # Return the dictionary


# Define a function that returns a dictionary with a constant indicating whether the recaptcha badge should be visible or not
def recaptchaBadge():
    """
    Returns a dictionary with a constant indicating whether the recaptcha badge should be visible or not.

    Returns:
        dict: A dictionary with a constant indicating whether the recaptcha badge should be visible or not.
    """

    # Define a nested function that checks the recaptcha and recaptcha badge constants
    def recaptchaBadge():
        # Use a match-case statement to return True or False based on the constants
        match RECAPTCHA and RECAPTCHA_BADGE:
            case True:  # If both constants are True, return True
                return True
            case False:  # If both constants are False, return False
                return False
            # No default case to handle other possible combinations of the constants

    return dict(recaptchaBadge=recaptchaBadge())  # Return the dictionary


# Define a function that returns a dictionary with the login enabled
def isLogin():
    """
    Returns a dictionary with a constant login is enabled or not.

    Returns:
        dict: A dictionary with a constant login is enabled or not.
    """

    return dict(isLogin=LOG_IN)  # Return the dictionary


# Define a function that returns a dictionary with the registration enabled
def isRegistration():
    """
    Returns a dictionary with a constant registration is enabled or not.

    Returns:
        dict: A dictionary with a constant registration is enabled or not.
    """

    return dict(isRegistration=REGISTRATION)  # Return the dictionary
