from flask import Blueprint, render_template
from utils.log import Log

searchBarBlueprint = Blueprint("searchBar", __name__)


@searchBarBlueprint.route("/searchbar")
def searchBar():
    """
    This function returns the search bar HTML page.

    Returns:
        The search bar HTML page.
    """

    Log.info("Rendering searchBar.html.jinja")
    return render_template("searchBar.html.jinja")
