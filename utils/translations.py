from modules import (
    Log,  # Importing the Log class from the modules module
    exists,  # Importing the exists function from the modules module
    load,  # Importing the load function from the modules module
)  # Importing the load, exists and Log functions from the modules module


def loadTranslations(language):
    """
    Load the translations for the specified language.

    Paremters:
        language (str): The language code for the translations to be loaded.

    Returns:
        dict: A dictionary containing the translations for the specified language.
    """

    translationFile = (
        f"./translations/{language}.json"  # Define the path to the translation file
    )
    match exists(translationFile):  # Check if the translation file exists
        case True:
            # If the translation file exists, open and load the JSON data
            with open(
                translationFile, "r", encoding="utf-8"
            ) as file:  # Open the translation file in read mode
                translations = load(file)  # Load the JSON data from the file
                Log.info(
                    f"Loaded translations for language: {language}"
                )  # Log a message indicating that the translations have been loaded
                return translations  # Return the translations as a dictionary
    Log.warning(
        f"Translation file not found: {language}"
    )  # Log a warning message if the translation file does not exist
    return {}  # Return an empty dictionary if the translation file does not exist
