from helpers import (
    sqlite3,
    flash,
    message,
    redirect,
    render_template,
    Blueprint,
)

searchBlueprint = Blueprint("search", __name__)


@searchBlueprint.route("/search/<query>", methods=["GET", "POST"])
def changeUserName(query):
    query = query.replace(" ", "")
    query = query.lower()
    connection = sqlite3.connect("db/posts.db")
    cursor = connection.cursor()
    queryTags = cursor.execute(
        f"select * from posts where tags like '%{query}%'"
    ).fetchall()
    queryTitles = cursor.execute(
        f"select * from posts where title like '%{query}%'"
    ).fetchall()
    posts = []
    match queryTags == []:
        case False:
            posts.append(queryTags)
    match queryTitles == []:
        case False:
            posts.append(queryTitles)
    return render_template("search.html", posts=posts, query=query)
