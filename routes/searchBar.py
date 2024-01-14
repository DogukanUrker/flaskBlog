from helpers import (
    Blueprint,
    render_template,
)

searchBarBlueprint = Blueprint("searchBar", __name__)


@searchBarBlueprint.route("/searchbar")
def searchBar():
    return render_template("searchBar.html")
