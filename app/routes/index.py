"""
This file contains the routes for the Flask application.

The Blueprint "index" is used to define the home page of the application.
The route "/" maps the index function to the home page.

The index function retrieves all posts from the database and passes them to the index.html template.

The posts variable is passed to the index.html template as a list of dictionaries.

The index.html template displays the title and content of each post.

DISCLAIMER: This code is the property of the repository owner and is not intended for
use without explicit permission from the owner. The code is provided as-is and is
subject to change without notice. Use of this code for commercial or non-commercial
purposes without permission is strictly prohibited.
"""

from json import load

from flask import Blueprint, redirect, render_template, session
from settings import Settings
from utils.log import Log
from utils.paginate import paginate_query

indexBlueprint = Blueprint("index", __name__)


@indexBlueprint.route("/")
@indexBlueprint.route("/by=<by>/sort=<sort>")
def index(by="hot", sort="desc"):
    """
    This function maps the home page route ("/") to the index function.

    It retrieves all posts from the database and passes them to the index.html template.

    The posts variable is passed to the index.html template as a list of dictionaries.

    The index.html template displays the title and content of each post.

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

    if by == "hot":
        select_query = (
            "SELECT *, (views * 1 / log(1 + (strftime('%s', 'now') - timeStamp) / 3600 + 2)) "
            f"AS hotScore FROM posts ORDER BY hotScore {sort}"
        )
    else:
        select_query = f"select * from posts order by {by} {sort}"

    posts, page, total_pages = paginate_query(
        Settings.DB_POSTS_ROOT,
        "select count(*) from posts",
        select_query,
    )

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
        "index.html",
        posts=posts,
        sortName=sortName,
        source="",
        page=page,
        total_pages=total_pages,
    )
