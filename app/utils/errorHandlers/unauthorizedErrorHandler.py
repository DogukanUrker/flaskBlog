from flask import render_template
from utils.log import Log


def unauthorizedErrorHandler(e):
    """
    This function returns a custom 401 page when a user tries to access a protected resource without proper authentication.

    :param e: The exception object
    :return: A tuple containing the Jinja template for the 401 error and the status code
    """

    Log.error(e)

    return render_template("unauthorized.html"), 401
