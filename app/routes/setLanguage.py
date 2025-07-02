from flask import Blueprint, redirect, session
from settings import LANGUAGES
from utils.flashMessage import flashMessage
from utils.log import Log

setLanguageBlueprint = Blueprint("setLanguage", __name__)


@setLanguageBlueprint.route("/setLanguage/<language>")
def setLanguage(language):
    """
    Set the language for the application.

    Parameters:
        language (str): The language code to set for the application.

    Returns:
        str: The selected language code."""
    if language in LANGUAGES:
        session["language"] = language
        Log.info(f"Language set to: {language}")
        flashMessage(
            page="setLanguage",
            message="success",
            category="success",
            language=session["language"],
        )
    else:
        Log.warning(f"Language not supported: {language}")
    return redirect("/changeLanguage")
