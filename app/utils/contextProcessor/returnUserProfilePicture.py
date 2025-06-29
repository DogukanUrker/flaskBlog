from utils.getProfilePicture import getProfilePicture


def returnUserProfilePicture():
    """
    Returns a dictionary with the user's profile picture URL.

    Returns:
        dict: A dictionary containing the user's profile picture URL.
    """

    return dict(getProfilePicture=getProfilePicture)
