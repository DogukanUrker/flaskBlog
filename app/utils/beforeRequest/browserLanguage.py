from flask import request, session
from settings import Settings
from utils.log import Log


def browserLanguage():
    """
    Set the user's language based on the browser's preferred language.

     Parameters:
        None

    Returns:
        None
    """
    if "language" not in session:
        browserLanguage = request.headers.get("Accept-Language")
        if browserLanguage:
            browserLanguage = browserLanguage.split(",")[0].split("-")[0]
            if browserLanguage in Settings.LANGUAGES:
                session["language"] = browserLanguage
                Log.info(f"Browser language detected and set to: {browserLanguage}")
            else:
                session["language"] = "en"
                Log.warning(
                    f"Browser language '{browserLanguage}' not supported. Defaulting to English."
                )
        else:
            session["language"] = "en"
            Log.warning("No browser language detected. Defaulting to English.")
    else:
        Log.info(f"Language already set in session: {session['language']}")
