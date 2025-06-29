from utils.generateUrlIdFromPost import getSlugFromPostTitle


def returnPostUrlSlug():
    """
    Returns a dictionary with the post's urlSlug.

    Returns:
        dict: A dictionary containing the post's urlSlug.
    """

    return dict(getSlugFromPostTitle=getSlugFromPostTitle)
