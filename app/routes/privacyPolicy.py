"""
This module contains the privacy policy page blueprint.
"""

from flask import Blueprint, render_template
from utils.log import Log  # A class for logging messages

# Create a blueprint object for the Privacy Policy page
privacyPolicyBlueprint = Blueprint("privacyPolicy", __name__)


# Define a route for the Privacy Policy page
@privacyPolicyBlueprint.route("/privacyPolicy")
def privacyPolicy():
    """
    This function is used to render the Privacy Policy page.

    :return: The rendered Privacy Policy page
    :rtype: flask.Response
    """

    # Use the Log module to log information to the console
    Log.info("Rendering privacyPolicy.html.jinja")

    # Use the render_template function to render the privacyPolicy.html.jinja file
    return render_template("privacyPolicy.html.jinja")
