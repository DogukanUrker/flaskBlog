from utils.getPostUrlIdFromPost import getPostUrlIdFromPost


def returnPostUrlID():
    """
    Returns a dictionary with the post's URL id.

    Returns:
        dict: A dictionary containing the post's URL id.
    """

    return dict(getPostUrlIdFromPost=getPostUrlIdFromPost)
