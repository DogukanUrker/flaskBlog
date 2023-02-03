from helpers import sqlite3, render_template, Blueprint, session, redirect

adminPanelPostsBlueprint = Blueprint("adminPanelPosts", __name__)


@adminPanelPostsBlueprint.route("/admin/posts")
@adminPanelPostsBlueprint.route("/adminpanel/posts")
def adminPanelPosts():
    match "userName" in session:
        case True:
            connection = sqlite3.connect("db/users.db")
            cursor = connection.cursor()
            cursor.execute(
                f'select role from users where userName = "{session["userName"]}"'
            )
            role = cursor.fetchone()[0]
            match role == "admin":
                case True:
                    connection = sqlite3.connect("db/posts.db")
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
