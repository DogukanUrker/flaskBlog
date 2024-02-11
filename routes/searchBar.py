# Import the necessary modules and functions
from modules import (
    Log,  # A class for logging messages
    Blueprint,  # A class for creating Flask blueprints
    render_template,  # A function for rendering Jinja templates
)


# Create a blueprint for the search bar route
searchBarBlueprint = Blueprint(
    "searchBar", __name__
)  # Pass the name of the blueprint and the current module name as arguments


@searchBarBlueprint.route("/searchbar")  # Define a route for the search bar page
def searchBar():
    """
    This function returns the search bar HTML page.

    Returns:
        The search bar HTML page.
    """
    # Use the Log module to log information to the console
    Log.info(f"Rendering searchBar.html.jinja")
    return render_template(
        "searchBar.html.jinja"
    )  # Return the rendered template of the search bar page
