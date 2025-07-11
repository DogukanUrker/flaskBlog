from utils.getPostUrlIdFromPost import get_post_url_id_from_post


def returnPostUrlID():
    """
    Returns a dictionary with the post's URL id.

    Returns:
        dict: A dictionary containing the post's URL id.
    """

    return dict(getPostUrlIdFromPost=get_post_url_id_from_post)
