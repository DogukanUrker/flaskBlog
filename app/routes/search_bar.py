from flask import Blueprint, render_template
from utils.log import Log

search_bar_blueprint = Blueprint("searchBar", __name__)


@search_bar_blueprint.route("/searchbar")
def search_bar():
    """
    This function returns the search bar HTML page.

    Returns:
        The search bar HTML page.
    """

    Log.info("Rendering searchBar.html")
    return render_template("searchBar.html")
