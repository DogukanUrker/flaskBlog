"""
This module contains the database delete functions for the app.

The functions in this module are responsible for managing the database
and interacting with the posts, users, and comments tables.

The functions in this module are:

- deletePost(postID): This function deletes a post and all associated comments
from the database.
- deleteUser(userName): This function deletes a user and all associated data
from the database.
- deleteComment(commentID): This function deletes a comment from the database.

The functions in this module use the following helper functions:

- flash(message, category): This function flashes a message to the user.
- message(type, message): This function sends a message to the server.
- session: This variable stores information about the current user's session.
- redirect(url): This function redirects the user to a new URL.
- DB_POSTS_ROOT: This variable stores the path to the posts database.
- DB_USERS_ROOT: This variable stores the path to the users database.
- DB_COMMENTS_ROOT: This variable stores the path to the comments database.
"""

from helpers import (
    flash,
    sqlite3,
    message,
    session,
    redirect,
    DB_POSTS_ROOT,
    DB_USERS_ROOT,
    DB_COMMENTS_ROOT,
)


def deletePost(postID):
    """
    This function deletes a post and all associated comments from the database.

    Parameters:
    postID (str): The ID of the post to be deleted.

    Returns:
    None
    """
    connection = sqlite3.connect(DB_POSTS_ROOT)
    cursor = connection.cursor()
    cursor.execute(
        """select author from posts where id = ? """,
        [(postID)],
    )
    cursor.execute(
        """delete from posts where id = ? """,
        [(postID)],
    )
    cursor.execute("update sqlite_sequence set seq = seq-1")
    connection.commit()
    connection.close()
    connection = sqlite3.connect(DB_COMMENTS_ROOT)
    cursor = connection.cursor()
    cursor.execute(
        """select count(*) from comments where post = ? """,
        [(postID)],
    )
    commentCount = list(cursor)[0][0]
    cursor.execute(
        """delete from comments where post = ? """,
        [(postID)],
    )
    cursor.execute(
        """update sqlite_sequence set seq = seq - ? """,
        [(commentCount)],
    )
    connection.commit()
    flash("post deleted", "error")
    message("2", f'POST: "{postID}" DELETED')


def deleteUser(userName):
    """
    This function deletes a user and all associated data from the database.

    Parameters:
    userName (str): The username of the user to be deleted.

    Returns:
    None
    """
    connection = sqlite3.connect(DB_USERS_ROOT)
    cursor = connection.cursor()
    cursor.execute(
        """select * from users where lower(userName) = ? """,
        [(userName.lower())],
    )
    cursor.execute(
        """select role from users where userName = ? """,
        [(session["userName"])],
    )
    perpetrator = cursor.fetchone()
    cursor.execute(
        """delete from users where lower(userName) = ? """,
        [(userName.lower())],
    )
    cursor.execute("update sqlite_sequence set seq = seq-1")
    connection.commit()
    flash(f"user: {userName} deleted", "error")
    message("2", f'USER: "{userName}" DELETED')
    match perpetrator[0] == "admin":
        case True:
            return redirect(f"/admin/users")
        case False:
            session.clear()
            return redirect(f"/")


def deleteComment(commentID):
    """
    This function deletes a comment from the database.

    Parameters:
    commentID (str): The ID of the comment to be deleted.

    Returns:
    None
    """
    connection = sqlite3.connect(DB_COMMENTS_ROOT)
    cursor = connection.cursor()
    cursor.execute(
        """select user from comments where id = ? """,
        [(commentID)],
    )
    cursor.execute(
        """delete from comments where id = ? """,
        [(commentID)],
    )
    cursor.execute("update sqlite_sequence set seq = seq-1")
    connection.commit()
    flash("comment deleted", "error")
    message("2", f'COMMENT: "{commentID}" DELETED')
