from helpers import (
    sqlite3,
    Blueprint,
    DB_POSTS_ROOT,
    render_template,
)

indexBlueprint = Blueprint("index", __name__)


@indexBlueprint.route("/")
def index():
    connection = sqlite3.connect(DB_POSTS_ROOT)
    cursor = connection.cursor()
    cursor.execute("select * from posts")
    posts = cursor.fetchall()
    return render_template(
        "index.html",
        posts=posts,
    )
