"""
This module contains the privacy policy page blueprint.
"""

from flask import Blueprint, render_template
from utils.log import Log

privacyPolicyBlueprint = Blueprint("privacyPolicy", __name__)


@privacyPolicyBlueprint.route("/privacyPolicy")
def privacyPolicy():
    """
    This function is used to render the Privacy Policy page.

    :return: The rendered Privacy Policy page
    :rtype: flask.Response
    """

    Log.info("Rendering privacyPolicy.html.jinja")

    return render_template("privacyPolicy.html.jinja")
