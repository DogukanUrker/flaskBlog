from flask import render_template
from utils.log import Log


# Define a function to handle CSRF errors
def csrfErrorHandler(e):
    """
    This function returns a custom 400 page when a CSRF token is invalid or missing.

    :param e: The exception object
    :return: A tuple containing the Jinja template for the 400 error and the status code
    """
    # Log a danger message with the error code and message
    Log.error(e)
    # Render the 400 template and pass the reason as a variable
    return render_template("csrfError.html.jinja", reason=e.description), 400
