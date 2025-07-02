from flask import Blueprint, render_template

changeLanguageBlueprint = Blueprint("changeLanguage", __name__)


@changeLanguageBlueprint.route("/changelanguage")
def changeLanguage():
    """
    Show the user's current language preference.

    Parameters:
        None

    Returns:
        html: The changeLanguage.html file.

    """
    return render_template("changeLanguage.html")
