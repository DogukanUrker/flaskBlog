"""
This module contains the code for the category route.

The category route is responsible for handling requests to view posts by category.
It also provides an interface for sorting the posts by various criteria.
"""

# Import necessary modules and functions from other files or libraries
from modules import (
    DB_POSTS_ROOT,  # Importing the constant that stores the path to the database file
    Blueprint,  # Importing the Blueprint class to create modular routes for the application
    Log,  # Importing the Log class for logging messages
    abort,  # Importing the abort function for handling errors and aborting requests
    load,  # Importing the load function for loading JSON data from files
    redirect,  # Importing the redirect function for redirecting requests,
    render_template,  # Importing the render_template function to render HTML templates with context
    session,  # Importing the session object to store user session data
    sqlite3,  # Importing the sqlite3 module to interact with SQLite databases
)

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

    # Original copy of by
    _by = by

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
        category=translations["categories"][category.lower()],
        sortName=sortName,
        source=f"/category/{category}",
        sortBy=_by,
        orderBy=sort,
        categoryBy=category,
    )
