"""
This file contains the routes for the Flask application.

The Blueprint "index" is used to define the home page of the application.
The route "/" maps the index function to the home page.

The index function retrieves all posts from the database and passes them to the index.html.jinja template.

The posts variable is passed to the index.html.jinja template as a list of dictionaries.

The index.html.jinja template displays the title and content of each post.

DISCLAIMER: This code is the property of the repository owner and is not intended for
use without explicit permission from the owner. The code is provided as-is and is
subject to change without notice. Use of this code for commercial or non-commercial
purposes without permission is strictly prohibited.
"""

import sqlite3
from json import load

from flask import Blueprint, redirect, render_template, session
from settings import DB_POSTS_ROOT
from utils.log import Log

indexBlueprint = Blueprint("index", __name__)


@indexBlueprint.route("/")
@indexBlueprint.route("/by=<by>/sort=<sort>")
def index(by="hot", sort="desc"):
    """
    This function maps the home page route ("/") to the index function.

    It retrieves all posts from the database and passes them to the index.html.jinja template.

    The posts variable is passed to the index.html.jinja template as a list of dictionaries.

    The index.html.jinja template displays the title and content of each post.

    Parameters:
    by (str): The field to sort by. Options are "timeStamp", "title", "views", "category", "lastEditTimeStamp", "hot".
    sort (str): The order to sort in. Options are "asc" or "desc".

    Returns:
    The rendered template of the home page with sorted posts according to the provided sorting options.
    """

    byOptions = ["timeStamp", "title", "views", "category", "lastEditTimeStamp", "hot"]
    sortOptions = ["asc", "desc"]

    if by not in byOptions or sort not in sortOptions:
        Log.warning(
            f"The provided sorting options are not valid: By: {by} Sort: {sort}"
        )
        return redirect("/")

    Log.database(f"Connecting to '{DB_POSTS_ROOT}' database")

    connection = sqlite3.connect(DB_POSTS_ROOT)
    connection.set_trace_callback(Log.database)

    cursor = connection.cursor()

    if by == "hot":
        cursor.execute(
            f"SELECT *, (views * 1 / log(1 + (strftime('%s', 'now') - timeStamp) / 3600 + 2)) AS hotScore FROM posts ORDER BY hotScore {sort}"
        )
        pass
    else:
        cursor.execute(f"select * from posts order by {by} {sort}")

    posts = cursor.fetchall()

    if by == "timeStamp":
        by = "create"
    elif by == "lastEditTimeStamp":
        by = "edit"

    language = session.get("language")
    translationFile = f"./translations/{language}.json"
    with open(translationFile, "r", encoding="utf-8") as file:
        translations = load(file)

    translations = translations["sortMenu"]

    sortName = translations[by] + " - " + translations[sort]

    Log.info(f"Sorting posts on index page by: {sortName}")

    return render_template(
        "index.html.jinja", posts=posts, sortName=sortName, source=""
    )
