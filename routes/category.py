# This file contains the code for the category page.

# The category page displays a list of all the posts in a specific category.
# It is accessible through the /category/<category> URL.

# The code in this file is organized as follows:

# 1. Import statements: The necessary modules are imported.

from helpers import (
    abort,  # A function to abort the request and return an error code
    sqlite3,  # A module to interact with SQLite databases
    Blueprint,  # A class to create modular routes for the application
    DB_POSTS_ROOT,  # A constant that stores the path to the database file
    render_template,  # A function to render a template with given context
)

# 2. Category blueprint: A blueprint for the category page is defined.

categoryBlueprint = Blueprint(
    "category", __name__
)  # Create a blueprint object with the name "category"

# 3. category route: The category route is defined, which takes a category
#    parameter. The route checks if the specified category exists, and if not,
#    returns a 404 error.


@categoryBlueprint.route(
    "/category/<category>"
)  # Define a route for the blueprint with a dynamic parameter <category>
def category(
    category,
):  # Define a function that handles the requests for the category route
    """
    This function returns the category page.

    Args:
        category (str): The category name.

    Returns:
        The category page as a template.

    Raises:
        404: If the specified category does not exist.
    """
    categories = [  # A list of valid categories
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
    match category.lower() in categories:  # Use the match statement to check if the category is in the list
        case False:  # If not, abort the request with a 404 error
            abort(404)
    connection = sqlite3.connect(DB_POSTS_ROOT)  # Connect to the database file
    cursor = connection.cursor()  # Create a cursor object to execute queries
    cursor.execute(  # Execute a query to select all the posts that belong to the given category
        """select * from posts where lower(category) = ? order by timeStamp desc""",
        [(category.lower())],  # Use a parameterized query to avoid SQL injection
    )
    posts = cursor.fetchall()  # Fetch all the results as a list of tuples
    return render_template(
        "category.html.jinja", posts=posts, category=category
    )  # Render the category template with the posts and the category as context
