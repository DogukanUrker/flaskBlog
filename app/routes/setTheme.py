from flask import Blueprint, redirect, request, session, url_for
from settings import Settings
from utils.log import Log

setThemeBlueprint = Blueprint("setTheme", __name__)


@setThemeBlueprint.route("/setTheme/<theme>")
def setTheme(theme):
    """
    Set the theme for the application.

    Parameters:
        theme (str): The theme name to set for the application.

    Returns:
        str: Redirect to the previous page or home.
    """
    if theme in Settings.THEMES:
        session["theme"] = theme
        Log.info(f"Theme set to: {theme}")
    else:
        Log.warning(f"Theme not supported: {theme}")

    # Redirect back to the page the user came from, or home if no referrer
    return redirect(request.referrer or url_for("index"))
