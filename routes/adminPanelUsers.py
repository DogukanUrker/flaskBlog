from helpers import sqlite3, render_template, Blueprint, session, redirect

adminPanelUsersBlueprint = Blueprint("adminPanelUsers", __name__)


@adminPanelUsersBlueprint.route("/admin/users")
@adminPanelUsersBlueprint.route("/adminpanel/users")
def adminPanelUsers():
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
                    connection = sqlite3.connect("db/users.db")
                    cursor = connection.cursor()
                    cursor.execute("select * from users")
                    users = cursor.fetchall()
                    connection = sqlite3.connect("db/posts.db")
                    cursor = connection.cursor()
                    cursor.execute("select * from posts")
                    posts = cursor.fetchall()
                    connection = sqlite3.connect("db/comments.db")
                    cursor = connection.cursor()
                    cursor.execute("select * from comments")
                    comments = cursor.fetchall()
                    return render_template(
                        "adminPanelUsers.html",
                        users=users,
                        posts=posts,
                        comments=comments,
                    )
                case False:
                    return redirect("/")
        case False:
            return redirect("/")
