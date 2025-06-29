# Import the function from utils module
from utils.getProfilePicture import getProfilePicture  # A function that returns the user's profile picture URL


# Define a function that returns a dictionary with the user's profile picture URL
def returnUserProfilePicture():
    """
    Returns a dictionary with the user's profile picture URL.

    Returns:
        dict: A dictionary containing the user's profile picture URL.
    """

    return dict(getProfilePicture=getProfilePicture)  # Return the dictionary
