"""
This file contains the blueprint and routes for the about page.
"""

from helpers import (
    APP_NAME,
    Blueprint,
    render_template,
)

aboutBlueprint = Blueprint("about", __name__)


@aboutBlueprint.route("/about")
def about():
    """
    This function is used to render the about page.

    :param appName: The name of the application
    :type appName: str
    :return: The rendered about page
    :rtype: flask.Response
    """
    return render_template("about.html.jinja", appName=APP_NAME)
