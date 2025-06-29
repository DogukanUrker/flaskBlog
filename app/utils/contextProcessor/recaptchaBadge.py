# Import the modules module that contains constants and functions for the app
from modules import (
    RECAPTCHA,  # A constant that indicates if the recaptcha is enabled
    RECAPTCHA_BADGE,  # A constant indicating whether the recaptcha badge should be visible or not
)


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
