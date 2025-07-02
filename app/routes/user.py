"""
This module contains the route for viewing user profiles.
"""

import sqlite3

from flask import Blueprint, render_template
from settings import DB_COMMENTS_ROOT, DB_POSTS_ROOT, DB_USERS_ROOT
from utils.log import Log

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
    Log.database(f"Connecting to '{DB_USERS_ROOT}' database")
    connection = sqlite3.connect(DB_USERS_ROOT)
    connection.set_trace_callback(Log.database)
    cursor = connection.cursor()
    cursor.execute("select userName from users")
    users = cursor.fetchall()
    """
    This if statement checks if the given username exists in the database.
    If the username exists, the function fetches the user details and the number of views their posts have received.
    It also fetches all the posts made by the user and all the comments made by the user.
    """
    if userName in str(users).lower():
        Log.success(f'User: "{userName}" found')
        cursor.execute(
            """select * from users where lower(userName) = ? """,
            [(userName)],
        )
        user = cursor.fetchone()
        Log.database(f"Connecting to '{DB_POSTS_ROOT}' database")
        connection = sqlite3.connect(DB_POSTS_ROOT)
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()
        cursor.execute(
            """select views from posts where author = ? order by timeStamp desc""",
            [(user[1])],
        )
        viewsData = cursor.fetchall()
        views = 0
        for view in viewsData:
            views += int(view[0])
        cursor.execute(
            """select * from posts where author = ? order by timeStamp desc""",
            [(user[1])],
        )
        posts = cursor.fetchall()
        connection = sqlite3.connect(DB_COMMENTS_ROOT)
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()
        cursor.execute(
            """select * from comments where lower(user) = ? """,
            [(userName.lower())],
        )
        comments = cursor.fetchall()
        """
        This if statement checks if the user has any posts or comments.
        If the user has any posts, the variable showPosts is set to True.
        If the user has any comments, the variable showComments is set to True.
        """
        if posts == []:
            showPosts = False
        else:
            showPosts = True
        if comments == []:
            showComments = False
        else:
            showComments = True
        Log.success(f'User: "{userName}"s data loaded')
        return render_template(
            "user.html",
            user=user,
            views=views,
            posts=posts,
            comments=comments,
            showPosts=showPosts,
            showComments=showComments,
        )
    else:
        Log.error(f'User: "{userName}" not found')
        return render_template("notFound.html")
