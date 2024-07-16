from modules import (
    render_template,
    Blueprint,
)  # Import the render_template and Blueprint modules

changeLanguageBlueprint = Blueprint(
    "changeLanguage", __name__
)  # Create a blueprint for the changeLanguage route


@changeLanguageBlueprint.route(
    "/changeLanguage"
)  # Create a route for the changeLanguage route
def changeLanguage():
    """
    Show the user's current language preference.

    Parameters:
        None

    Returns:
        html: The changeLanguage.html.jinja file.

    """
    return render_template(
        "changeLanguage.html.jinja"
    )  # Render the changeLanguage template
