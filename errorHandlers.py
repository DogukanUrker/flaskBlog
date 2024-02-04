# Import the message and render_template functions from the helpers module
from helpers import message, render_template


# Define a function to handle 404 errors
def notFoundErrorHandler(e):
    """
    This function returns a custom 404 page when a requested resource is not found.

    :param e: The exception object
    :return: A tuple containing the Jinja template for the 404 error and the status code
    """
    # Log a danger message with the error code and message
    message("1", f"404 | {e}")
    # Render the 404 template and return it with the status code
    return render_template("notFound.html.jinja"), 404


# Define a function to handle unauthorized access errors
def unauthorizedErrorHandler(e):
    """
    This function returns a custom 401 page when a user tries to access a protected resource without proper authentication.

    :param e: The exception object
    :return: A tuple containing the Jinja template for the 401 error and the status code
    """
    # Log a danger message with the error code and message
    message("1", f"401 | {e}")
    # Render the 401 template and return it with the status code
    return render_template("unauthorized.html.jinja"), 401


# Define a function to handle CSRF errors
def csrfErrorHandler(e):
    """
    This function returns a custom 400 page when a CSRF token is invalid or missing.

    :param e: The exception object
    :return: A tuple containing the Jinja template for the 400 error and the status code
    """
    # Log a danger message with the error code and message
    message("1", f"400 | {e}")
    # Render the 400 template and pass the reason as a variable
    return render_template("csrfError.html.jinja", reason=e.description), 400
