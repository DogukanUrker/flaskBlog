"""
This file contains the routes for the Flask application.

The Blueprint "index" is used to define the home page of the application.
The route "/" maps the index function to the home page.

The index function retrieves all posts from the database and passes them to the index.html.jinja template.

The posts variable is passed to the index.html.jinja template as a list of dictionaries.

The index.html.jinja template displays the title and content of each post.
"""

from modules import (
    Log,  # A class for logging messages
    sqlite3,  # Importing the SQLite module for working with SQLite databases
    redirect,  # Importing the redirect function for redirecting requests
    Blueprint,  # Importing the Blueprint class for creating Flask blueprints
    DB_POSTS_ROOT,  # Importing the constant for the path to the posts database
    render_template,  # Importing the render_template function for rendering Jinja templates
)

# Create a blueprint for the home page with the name "index" and the current module name
indexBlueprint = Blueprint("index", __name__)


# Define a route for the home page
@indexBlueprint.route("/")
# Define a route for the home page with sorting parameters
@indexBlueprint.route("/by=<by>/sort=<sort>")
def index(by="timeStamp", sort="desc"):
    """
    This function maps the home page route ("/") to the index function.

    It retrieves all posts from the database and passes them to the index.html.jinja template.

    The posts variable is passed to the index.html.jinja template as a list of dictionaries.

    The index.html.jinja template displays the title and content of each post.

    Parameters:
    by (str): The field to sort by. Options are "timeStamp", "title", "views", "category", "lastEditTimeStamp".
    sort (str): The order to sort in. Options are "asc" or "desc".

    Returns:
    The rendered template of the home page with sorted posts according to the provided sorting options.
    """

    # Define valid options for sorting and filtering
    byOptions = ["timeStamp", "title", "views", "category", "lastEditTimeStamp"]
    sortOptions = ["asc", "desc"]

    # Check if the provided sorting options are valid, if not, redirect to the default route
    match by not in byOptions or sort not in sortOptions:
        case True:
            Log.warning(
                f"The provided sorting options are not valid: By: {by} Sort: {sort}"
            )
            return redirect("/")

    Log.sql(
        f"Connecting to '{DB_POSTS_ROOT}' database"
    )  # Log the database connection is started
    # Connect to the posts database
    connection = sqlite3.connect(DB_POSTS_ROOT)
    connection.set_trace_callback(Log.sql)  # Set the trace callback for the connection
    # Create a cursor object for executing queries
    cursor = connection.cursor()
    # Select all the columns from the posts table and order them by the specified field and sorting order
    cursor.execute(f"select * from posts order by {by} {sort}")
    # Fetch all the results as a list of tuples
    posts = cursor.fetchall()

    # Modify the sorting name for better readability
    match by:
        case "timeStamp":
            by = "Creation Date"
        case "lastEditTimeStamp":
            by = "Last Edit Date"
    sortName = f"{by} {sort}".title()

    # Log a info message that posts sorted by the specified field
    Log.info(f"Sorting posts on index page by: {sortName}")

    # Return the rendered template of the home page and pass the posts list and sorting name as keyword arguments
    return render_template(
        "index.html.jinja", posts=posts, sortName=sortName, source=""
    )
