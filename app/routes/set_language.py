from flask import Blueprint, redirect, request, session
from utils.flash_message import flash_message
from utils.log import Log

set_language_blueprint = Blueprint("setLanguage", __name__)


@set_language_blueprint.route("/setLanguage/<language>")
def set_language(language):
    """
    Set the language for the application.

    Parameters:
        language (str): The language code to set for the application.

    Returns:
        str: The selected language code."""
    if language in Settings.LANGUAGES:
        session["language"] = language
        Log.info(f"Language set to: {language}")
        flash_message(
            page="setLanguage",
            message="success",
            category="success",
            language=session["language"],
        )
    else:
        Log.warning(f"Language not supported: {language}")
    return redirect("/changelanguage")
