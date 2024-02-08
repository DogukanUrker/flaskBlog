# Import the message and render_template functions from the modules module
from modules import message, render_template


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
