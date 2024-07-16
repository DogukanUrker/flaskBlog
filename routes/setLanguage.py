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


@setLanguageBlueprint.context_processor
def injectTranslations():
    """
    Inject translations into the context of the application.

    Parameters:
        None

    Returns:
        dict: A dictionary containing the translations for the current language.
    """
    language = session.get(
        "language", "en"
    )  # Get the current language from the session
    translations = loadTranslations(
        language
    )  # Load the translations for the current language
    Log.info(f"Injecting translations for language: {language}")
    return dict(translations=translations)  # Return the translations as a dictionary


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


@setLanguageBlueprint.before_request
def beforeRequest():
    """
    Set the user's language based on the browser's preferred language.

     Parameters:
        None

    Returns:
        None
    """
    if "language" not in session:
        # Check if the user's language is not already set in the session
        browserLanguage = request.headers.get(
            "Accept-Language"
        )  # Get the browser's Accept-Language header
        if browserLanguage:
            # If the Accept-Language header is present, parse the first preferred language
            browserLanguage = browserLanguage.split(",")[0].split("-")[0]
            match browserLanguage:
                case lang if lang in LANGUAGES:
                    session["language"] = (
                        lang  # Set the session language to the browser's preferred language
                    )
                    Log.info(f"Browser language detected and set to: {lang}")
                case _:
                    session["language"] = (
                        "en"  # Default to English if the preferred language is not supported
                    )
                    Log.warning(
                        f"Browser language '{browserLanguage}' not supported. Defaulting to English."
                    )
        else:
            session["language"] = (
                "en"  # Default to English if the Accept-Language header is not present
            )
            Log.warning("No browser language detected. Defaulting to English.")
    else:
        Log.info(f"Language already set in session: {session['language']}")


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
