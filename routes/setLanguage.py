# Import necessary modules
from modules import (
    session,  # Session module for managing user sessions
    request,  # Request module for handling HTTP requests
    redirect,  # Redirect module for redirecting to different routes
    url_for,  # URL module for generating URLs for routes
    LANGUAGES,  # List of supported languages
    Log,  # Logging module for logging messages
    Blueprint,  # Blueprint module for creating route blueprints
    render_template,  # Template module for rendering HTML templates
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
        case _:
            Log.warning(f"Language not supported: {language}")
    return language


@setLanguageBlueprint.route("/changeLanguage")
def changeLanguage():
    """
    Show the user's current language preference.

    Parameters:
        None

    Returns:
        html: The changeLanguage html.jinja file.

    """
    return render_template(
        "changeLanguage.html.jinja"
    )  # Render the showLanguage template
