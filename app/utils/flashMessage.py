from json import load
from os.path import exists

from flask import flash


def flashMessage(page="error", message="wrongCall", category="error", language="en"):
    """
    Displays a flash message on the page.

    Args:
        page (str, optional): The page where the flash message will be displayed. Defaults to "error".
        message (str, optional): The specific message to be displayed. Defaults to "wrongCall".
        category (str, optional): The category of the flash message. Defaults to "error".
        language (str, optional): The language used for translation. Defaults to "en".

    Returns:
        None
    """
    text = None
    translationFile = f"./translations/{language}.json"
    match exists(translationFile):
        case True:
            with open(translationFile, "r", encoding="utf-8") as file:
                translations = load(file)
                text = translations["flash"]
    flash(text[page][message], category)
    return None
