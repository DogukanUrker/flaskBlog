from settings import Settings


def isLogin():
    """
    Returns a dictionary with a constant login is enabled or not.

    Returns:
        dict: A dictionary with a constant login is enabled or not.
    """

    return dict(isLogin=Settings.LOG_IN)
