from helpers import (
    render_template,
    Blueprint,
)

searchBarBlueprint = Blueprint("searchBar", __name__)


@searchBarBlueprint.route("/searchbar")
def searchBar():
    return render_template("searchBar.html")
