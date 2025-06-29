from flask import render_template
from utils.log import Log


# Define a function to handle 404 errors
def notFoundErrorHandler(e):
    """
    This function returns a custom 404 page when a requested resource is not found.

    :param e: The exception object
    :return: A tuple containing the Jinja template for the 404 error and the status code
    """
    # Log a danger message with the error code and message
    Log.error(e)
    # Render the 404 template and return it with the status code
    return render_template("notFound.html.jinja"), 404
