from modules import LANGUAGES, Log, request, session  # Import necessary modules


def browserLanguage():
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
