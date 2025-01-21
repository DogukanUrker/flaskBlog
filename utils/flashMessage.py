from modules import (
    load,  # Import the load function from the modules module
    flash,  # Import the flash function from the modules module
    exists,  # Import the exists function from the modules module
)  # Import the required functions from the modules module


def flashMessage(
    page="error", message="wrongCall", category="error", language="en"
):  # Define the flashMessage function
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
    text = None  # Initialize the text variable
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
                text = translations["flash"]  # Return the translations as a dictionary
    flash(text[page][message], category)  # Display the flash message on the page
    return None  # Return None
