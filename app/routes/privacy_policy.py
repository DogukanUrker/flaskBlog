"""
This module contains the privacy policy page blueprint.
"""

from flask import Blueprint, render_template
from utils.log import Log

privacy_policy_blueprint = Blueprint("privacyPolicy", __name__)


@privacy_policy_blueprint.route("/privacyPolicy")
def privacy_policy():
    """
    This function is used to render the Privacy Policy page.

    :return: The rendered Privacy Policy page
    :rtype: flask.Response
    """

    Log.info("Rendering privacyPolicy.html")

    return render_template("privacyPolicy.html")
