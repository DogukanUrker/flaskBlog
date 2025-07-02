from flask import render_template
from utils.log import Log


def notFoundErrorHandler(e):
    """
    This function returns a custom 404 page when a requested resource is not found.

    :param e: The exception object
    :return: A tuple containing the Jinja template for the 404 error and the status code
    """

    Log.error(e)

    return render_template("notFound.html"), 404
