# Import necessary modules
from modules import (
    flashMessage,  # Flash module for flashing messages to the user
    session,  # Session module for managing user sessions
    LANGUAGES,  # List of supported languages
    redirect,  # Redirect module for redirecting to routes
    Log,  # Logging module for logging messages
    Blueprint,  # Blueprint module for creating route blueprints
)
from utils.translations import loadTranslations  # Load translations for the application

# Create a blueprint for the search bar route
setLanguageBlueprint = Blueprint(
    "setLanguage", __name__
)  # Pass the name of the blueprint and the current module name as arguments


@setLanguageBlueprint.route("/setLanguage/<language>")
def setLanguage(language):
    """
    Set the language for the application.

    Parameters:
        language (str): The language code to set for the application.

    Returns:
        str: The selected language code."""
    match language:
        case lang if lang in LANGUAGES:
            session["language"] = (
                language  # Set the session language to the selected language
            )
            Log.info(f"Language set to: {language}")
            flashMessage(
                page="setLanguage",
                message="success",
                category="success",
                language=session["language"],
            )  # Display a flash message
        case _:
            Log.warning(f"Language not supported: {language}")
    return redirect("/changeLanguage")  # Redirect to the changeLanguage route
