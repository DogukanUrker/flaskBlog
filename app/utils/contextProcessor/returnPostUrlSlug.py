from utils.generateUrlIdFromPost import get_slug_from_post_title


def returnPostUrlSlug():
    """
    Returns a dictionary with the post's urlSlug.

    Returns:
        dict: A dictionary containing the post's urlSlug.
    """

    return dict(get_slug_from_post_title=get_slug_from_post_title)
