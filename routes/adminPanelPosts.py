from helpers import (
    sqlite3,
    session,
    request,
    redirect,
    Blueprint,
    DB_POSTS_ROOT,
    DB_USERS_ROOT,
    render_template,
)
from delete import deletePost

adminPanelPostsBlueprint = Blueprint("adminPanelPosts", __name__)


@adminPanelPostsBlueprint.route("/admin/posts", methods=["GET", "POST"])
@adminPanelPostsBlueprint.route("/adminpanel/posts", methods=["GET", "POST"])
def adminPanelPosts():
    match "userName" in session:
        case True:
            connection = sqlite3.connect(DB_USERS_ROOT)
            cursor = connection.cursor()
            cursor.execute(
                """select role from users where userName = ? """,
                [(session["userName"])],
            )
            role = cursor.fetchone()[0]
            match request.method == "POST":
                case True:
                    match "postDeleteButton" in request.form:
                        case True:
                            deletePost(request.form["postID"])
            match role == "admin":
                case True:
                    connection = sqlite3.connect(DB_POSTS_ROOT)
                    cursor = connection.cursor()
                    cursor.execute("select * from posts")
                    posts = cursor.fetchall()
                    return render_template(
                        "dashboard.html", posts=posts, showPosts=True
                    )
                case False:
                    return redirect("/")
        case False:
            return redirect("/")
