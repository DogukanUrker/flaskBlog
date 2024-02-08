from helpers import (
    sqlite3,
    render_template,
    Blueprint,
)

indexBlueprint = Blueprint("index", __name__)


@indexBlueprint.route("/")
def index():
    connection = sqlite3.connect("db/posts.db")
    cursor = connection.cursor()
    cursor.execute("select * from posts")
    posts = cursor.fetchall()
    return render_template(
        "index.html",
        posts=posts,
    )
