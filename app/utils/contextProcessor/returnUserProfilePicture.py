from utils.getProfilePicture import get_profile_picture


def returnUserProfilePicture():
    """
    Returns a dictionary with the user's profile picture.

    Returns:
        dict: A dictionary containing the user's profile picture.
    """

    return dict(getProfilePicture=get_profile_picture)
