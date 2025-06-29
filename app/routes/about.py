"""
This module contains the about page blueprint.
"""

from flask import Blueprint, render_template
from settings import APP_NAME, APP_VERSION
from utils.log import Log

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

    Log.info(
        f"Rendering about.html: params: appName={APP_NAME} and appVersion={APP_VERSION}"
    )

    return render_template("about.html", appName=APP_NAME, appVersion=APP_VERSION)
