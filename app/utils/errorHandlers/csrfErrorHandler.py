from flask import render_template
from utils.log import Log


def csrfErrorHandler(e):
    """
    This function returns a custom 400 page when a CSRF token is invalid or missing.

    :param e: The exception object
    :return: A tuple containing the Jinja template for the 400 error and the status code
    """

    Log.error(e)

    return render_template("csrfError.html", reason=e.description), 400
