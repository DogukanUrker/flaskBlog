"""
This module contains the route for category pages.
"""

"""
DISCLAIMER: This code is the property of the repository owner and is not intended for 
use without explicit permission from the owner. The code is provided as-is and is 
subject to change without notice. Use of this code for commercial or non-commercial 
purposes without permission is strictly prohibited.
"""

import sqlite3
from json import load  # Importing the load function for loading JSON data from files
from flask import Blueprint, render_template, request, redirect, session, abort
from constants import DB_POSTS_ROOT
from utils.log import Log

# Creating a Blueprint object named 'categoryBlueprint' for this route
categoryBlueprint = Blueprint("category", __name__)


# Decorator to define the route for viewing posts by category
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
    # List of available categories
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

    # List of available options for sorting
    byOptions = ["timeStamp", "title", "views", "category", "lastEditTimeStamp"]
    sortOptions = ["asc", "desc"]

    # Checking if provided sorting options are valid
    match by not in byOptions or sort not in sortOptions:
        case True:
            Log.warning(
                f"The provided sorting options are not valid: By: {by} Sort: {sort}"
            )
            return redirect(f"/category/{category}")

    # Check if the requested category is valid
    match category.lower() in categories:
        case False:
            abort(404)

    Log.database(
        f"Connecting to '{DB_POSTS_ROOT}' database"
    )  # Log the database connection is started

    # Establishing a connection to the SQLite database
    connection = sqlite3.connect(DB_POSTS_ROOT)
    connection.set_trace_callback(
        Log.database
    )  # Set the trace callback for the connection
    cursor = connection.cursor()

    # Executing SQL query to retrieve posts of the requested category and sorting them accordingly
    cursor.execute(
        f"""select * from posts where lower(category) = ? order by {by} {sort}""",
        [(category.lower())],
    )
    posts = cursor.fetchall()

    # Modify the sorting name for better readability
    match by:
        case "timeStamp":
            by = "create"
        case "lastEditTimeStamp":
            by = "edit"

    language = session.get("language")  # Get the language from the session
    translationFile = (
        f"./translations/{language}.json"  # Define the path to the translation file
    )
    with open(
        translationFile, "r", encoding="utf-8"
    ) as file:  # Open the translation file in read mode
        translations = load(file)  # Load the JSON data from the file

    sortName = (
        translations["sortMenu"][by] + " - " + translations["sortMenu"][sort]
    )  # Get the sorting name from the translations

    # Logging the sorting criteria used for the request
    Log.info(f"Sorting posts on category/{category} page by: {sortName}")

    # Rendering the HTML template with posts and category context
    return render_template(
        "category.html.jinja",
        posts=posts,
        category=translations["categories"][category.lower()],
        sortName=sortName,
        source=f"/category/{category}",
    )
