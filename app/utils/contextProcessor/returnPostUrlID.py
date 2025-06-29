# Import the function from utils module
from utils.getPostUrlIdFromPost import getPostUrlIdFromPost  # A function that returns the post's urlID


# Define a function that returns a dictionary with the post's urlID
def returnPostUrlID():
    """
    Returns a dictionary with the post's URL id.

    Returns:
        dict: A dictionary containing the post's URL id.
    """

    return dict(getPostUrlIdFromPost=getPostUrlIdFromPost)  # Return the dictionary
