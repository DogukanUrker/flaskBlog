"""
This module contains the route for category pages.

DISCLAIMER: This code is the property of the repository owner and is not intended for
use without explicit permission from the owner. The code is provided as-is and is
subject to change without notice. Use of this code for commercial or non-commercial
purposes without permission is strictly prohibited.
"""

import sqlite3
from json import load

from flask import Blueprint, abort, redirect, render_template, session
from settings import DB_POSTS_ROOT
from utils.log import Log

categoryBlueprint = Blueprint("category", __name__)


@categoryBlueprint.route("/category/<category>")
@categoryBlueprint.route("/category/<category>/by=<by>/sort=<sort>")
def category(category, by="timeStamp", sort="desc"):
    """
    This function handles requests for the category route.

    :param category: The category name that is requested
    :param by: The field to sort the posts by
    :param sort: The sorting order of the posts
    :return: A rendered template with the posts and the category as context
    """

    categories = [
        "games",
        "history",
        "science",
        "code",
        "technology",
        "education",
        "sports",
        "foods",
        "health",
        "apps",
        "movies",
        "series",
        "travel",
        "books",
        "music",
        "nature",
        "art",
        "finance",
        "business",
        "web",
        "other",
    ]

    byOptions = ["timeStamp", "title", "views", "category", "lastEditTimeStamp"]
    sortOptions = ["asc", "desc"]

    if by not in byOptions or sort not in sortOptions:
        Log.warning(
            f"The provided sorting options are not valid: By: {by} Sort: {sort}"
        )
        return redirect(f"/category/{category}")

    if category.lower() not in categories:
        abort(404)

    Log.database(f"Connecting to '{DB_POSTS_ROOT}' database")

    connection = sqlite3.connect(DB_POSTS_ROOT)
    connection.set_trace_callback(Log.database)
    cursor = connection.cursor()

    cursor.execute(
        f"""select * from posts where lower(category) = ? order by {by} {sort}""",
        [(category.lower())],
    )
    posts = cursor.fetchall()

    if by == "timeStamp":
        by = "create"
    elif by == "lastEditTimeStamp":
        by = "edit"

    language = session.get("language")
    translationFile = f"./translations/{language}.json"
    with open(translationFile, "r", encoding="utf-8") as file:
        translations = load(file)

    sortName = translations["sortMenu"][by] + " - " + translations["sortMenu"][sort]

    Log.info(f"Sorting posts on category/{category} page by: {sortName}")

    return render_template(
        "category.html",
        posts=posts,
        category=translations["categories"][category.lower()],
        sortName=sortName,
        source=f"/category/{category}",
    )
