from flask import Blueprint, render_template

change_language_blueprint = Blueprint("changeLanguage", __name__)


@change_language_blueprint.route("/changelanguage")
def change_language():
    """
    Show the user's current language preference.

    Parameters:
        None

    Returns:
        html: The changeLanguage.html file.

    """
    return render_template("changeLanguage.html")
