# Import the message and render_template functions from the helpers module
from helpers import message, render_template


# Define a function to handle 404 errors
def notFoundErrorHandler(e):
    """
    This function handles 404 errors

    :param e: The exception object
    :return: A tuple containing the Jinja template for the 404 error and the status code
    """
    # Log a danger message with 404 error
    message("1", "404 | NOT FOUND")
    # Render a template for 404 errors and return it with a 404 status code
    return render_template("404.html.jinja"), 404


# Define a function to handle unauthorized access errors
def unauthorizedErrorHandler(e):
    """
    This function handles 401 errors, which are unauthorized access errors.

    :param e: The exception object
    :return: A tuple containing the Jinja template for the 401 error and the status code
    """
    # Log a danger message with 401 error
    message("1", "401 | UNAUTHORIZED ERROR")
    # Render a template for 401 errors and return it with a 401 status code
    return render_template("401.html.jinja"), 401


# Define a function to handle CSRF errors
def csrfErrorErrorHandler(e):
    """
    This function handles 400 errors, which are CSRF errors.

    :param e: The exception object
    :return: A tuple containing the Jinja template for the 400 error and the status code
    """
    # Log a danger message with 400 error
    message("1", "400 | CSRF ERROR")
    # Render a template for CSRF errors and pass the reason as a variable
    return render_template("csrfError.html.jinja", reason=e.description), 400
