from helpers import (
    sqlite3,
    message,
    Blueprint,
    DB_POSTS_ROOT,
    DB_USERS_ROOT,
    render_template,
    DB_COMMENTS_ROOT,
)

userBlueprint = Blueprint("user", __name__)


@userBlueprint.route("/user/<userName>")
def user(userName):
    connection = sqlite3.connect(DB_USERS_ROOT)
    cursor = connection.cursor()
    cursor.execute(f"select userName from users")
    users = cursor.fetchall()
    match str(userName).lower() in str(users).lower():
        case True:
            message("2", f'USER: "{userName}" FOUND')
            cursor.execute(
                """select * from users where lower(userName) = ? """,
                [(userName)],
            )
            user = cursor.fetchone()
            connection = sqlite3.connect(DB_POSTS_ROOT)
            cursor = connection.cursor()
            cursor.execute(
                """select views from posts where author = ? """,
                [(user[1])],
            )
            viewsData = cursor.fetchall()
            views = 0
            for view in viewsData:
                views += int(view[0])
            cursor.execute(
                """select * from posts where author = ? """,
                [(user[1])],
            )
            posts = cursor.fetchall()
            connection = sqlite3.connect(DB_COMMENTS_ROOT)
            cursor = connection.cursor()
            cursor.execute(
                """select * from comments where lower(user) = ? """,
                [(userName.lower())],
            )
            comments = cursor.fetchall()
            match posts:
                case []:
                    showPosts = False
                case _:
                    showPosts = True
            match comments:
                case []:
                    showComments = False
                case _:
                    showComments = True
            message("2", f'USER: "{userName}"s PAGE LOADED')
            return render_template(
                "user.html",
                user=user,
                views=views,
                posts=posts,
                comments=comments,
                showPosts=showPosts,
                showComments=showComments,
            )
        case _:
            message("1", f'USER: "{userName}" NOT FOUND')
            return render_template("404.html")
