"""
This module contains the code for the category route.

The category route is responsible for handling requests to view posts by category.
It also provides an interface for sorting the posts by various criteria.
"""

# Import necessary modules and functions from other files or libraries
from modules import (
    Log,  # Importing the Log class for logging messages
    abort,  # Importing the abort function for handling errors and aborting requests
    sqlite3,  # Importing the sqlite3 module to interact with SQLite databases
    redirect,  # Importing the redirect function for redirecting requests
    Blueprint,  # Importing the Blueprint class to create modular routes for the application
    DB_POSTS_ROOT,  # Importing the constant that stores the path to the database file
    render_template,  # Importing the render_template function to render HTML templates with context
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

    Log.sql(
        f"Connecting to '{DB_POSTS_ROOT}' database"
    )  # Log the database connection is started

    # Establishing a connection to the SQLite database
    connection = sqlite3.connect(DB_POSTS_ROOT)
    connection.set_trace_callback(Log.sql)  # Set the trace callback for the connection
    cursor = connection.cursor()

    # Executing SQL query to retrieve posts of the requested category and sorting them accordingly
    cursor.execute(
        f"""select * from posts where lower(category) = ? order by {by} {sort}""",
        [(category.lower())],
    )
    posts = cursor.fetchall()

    # Human-readable name for the sorting parameter
    match by:
        case "timeStamp":
            by = "Creation Date"
        case "lastEditTimeStamp":
            by = "Last Edit Date"
    sortName = f"{by} {sort}".title()

    # Logging the sorting criteria used for the request
    Log.info(f"Sorting posts on category/{category} page by: {sortName}")

    # Rendering the HTML template with posts and category context
    return render_template(
        "category.html.jinja",
        posts=posts,
        category=category,
        sortName=sortName,
        source=f"/category/{category}",
    )
