from settings import LOG_IN


def isLogin():
    """
    Returns a dictionary with a constant login is enabled or not.

    Returns:
        dict: A dictionary with a constant login is enabled or not.
    """

    return dict(isLogin=LOG_IN)
