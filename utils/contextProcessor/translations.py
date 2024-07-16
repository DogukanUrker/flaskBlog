from modules import session, Log  # Import the session and Log from the modules file
from ..translations import (
    loadTranslations,
)  # Load translations for the current language


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
