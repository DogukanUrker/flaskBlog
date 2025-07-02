from settings import Settings


def isRegistration():
    """
    Returns a dictionary with a constant registration is enabled or not.

    Returns:
        dict: A dictionary with a constant registration is enabled or not.
    """

    return dict(isRegistration=Settings.REGISTRATION)
