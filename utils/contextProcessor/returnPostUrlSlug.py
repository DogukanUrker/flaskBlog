# Import the modules module that contains constants and functions for the app
from modules import (
    getSlugFromPostTitle,  # A function that returns the post's urlSlug
)


# Define a function that returns a dictionary with the post's urlSlug
def returnPostUrlSlug():
    """
    Returns a dictionary with the post's urlSlug.

    Returns:
        dict: A dictionary containing the post's urlSlug.
    """

    return dict(getSlugFromPostTitle=getSlugFromPostTitle)  # Return the dictionary
