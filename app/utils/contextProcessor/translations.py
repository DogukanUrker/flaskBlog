from flask import session
from utils.log import Log

from ..translations import (
    loadTranslations,
)


def injectTranslations():
    """
    Inject translations into the context of the application.

    Parameters:
        None

    Returns:
        dict: A dictionary containing the translations for the current language.
    """
    language = session.get("language", "en")
    translations = loadTranslations(language)
    Log.info(f"Injecting translations for language: {language}")
    return dict(translations=translations)
