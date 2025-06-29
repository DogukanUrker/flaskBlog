"""
This module contains the about page blueprint.
"""

from flask import Blueprint, render_template
from constants import APP_NAME, APP_VERSION
from utils.log import Log  # A class for logging messages

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
    # Use the Log module to log information to the console
    Log.info(
        f"Rendering about.html.jinja: params: appName={APP_NAME} and appVersion={APP_VERSION}"
    )
    # Use the render_template function to render the about.html.jinja file
    # Pass the appName and appVersion variables to the template
    return render_template("about.html.jinja", appName=APP_NAME, appVersion=APP_VERSION)
