# This file contains the blueprint and routes for the Privacy Policy page.

# Import the necessary modules from the helpers file
from helpers import (
    Blueprint,  # A class that represents a Flask blueprint
    render_template,  # A function that renders a template file
)

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
    # Use the render_template function to render the privacyPolicy.html.jinja file
    return render_template("privacyPolicy.html.jinja")
