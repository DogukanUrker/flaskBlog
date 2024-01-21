# Import the necessary modules and functions
from helpers import (
    Blueprint,
    render_template,
)


# Create a blueprint for the search bar route
searchBarBlueprint = Blueprint("searchBar", __name__)


@searchBarBlueprint.route("/searchbar")
def searchBar():
    """
    This function returns the search bar HTML page.

    Returns:
        The search bar HTML page.
    """
    return render_template("searchBar.html")
