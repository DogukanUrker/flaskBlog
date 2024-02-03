"""
This module contains the code for the user page.
"""

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
    """
    This function is used to render the user page.

    :param userName: The username of the user.
    :type userName: str
    :return: The rendered user page.
    :rtype: flask.Response
    """
    userName = userName.lower()
    connection = sqlite3.connect(DB_USERS_ROOT)
    cursor = connection.cursor()
    cursor.execute(f"select userName from users")
    users = cursor.fetchall()
    """
    This match statement checks if the given username exists in the database.
    If the username exists, the function fetches the user details and the number of views their posts have received.
    It also fetches all the posts made by the user and all the comments made by the user.
    """
    match userName in str(users).lower():
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
            """
            This match statement checks if the user has any posts or comments.
            If the user has any posts, the variable showPosts is set to True.
            If the user has any comments, the variable showComments is set to True.
            """
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
                "user.html.jinja",
                user=user,
                views=views,
                posts=posts,
                comments=comments,
                showPosts=showPosts,
                showComments=showComments,
            )
        case _:
            message("1", f'USER: "{userName}" NOT FOUND')
            return render_template("notFound.html.jinja")
