# This file contains the blueprint and routes for the about page.

# Import the necessary modules from the helpers file
from helpers import (
    APP_NAME,  # A constant that stores the name of the application
    Blueprint,  # A class that represents a Flask blueprint
    APP_VERSION,  # A constant that stores the version of the application
    render_template,  # A function that renders a template file
)

# Create a blueprint object for the about page
aboutBlueprint = Blueprint("about", __name__)


# Define a route for the about page
@aboutBlueprint.route("/about")
def about():
    """
    This function is used to render the about page.

    :param appName: The name of the application
    :type appName: str
    :return: The rendered about page
    :rtype: flask.Response
    """
    # Use the render_template function to render the about.html.jinja file
    # Pass the appName and appVersion variables to the template
    return render_template("about.html.jinja", appName=APP_NAME, appVersion=APP_VERSION)
