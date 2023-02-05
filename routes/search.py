from helpers import (
    flash,
    message,
    redirect,
    render_template,
    Blueprint,
)

searchBlueprint = Blueprint("search", __name__)


@searchBlueprint.route("/search/<query>", methods=["GET", "POST"])
def changeUserName(query):
    query = query.replace("+", " ")
    print(query)
    return render_template("search.html")
