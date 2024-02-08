"""
This file contains the routes for the Flask application.

The Blueprint "index" is used to define the home page of the application.
The route "/" maps the index function to the home page.

The index function retrieves all posts from the database and passes them to the index.html.jinja template.

The posts variable is passed to the index.html.jinja template as a list of dictionaries.

The index.html.jinja template displays the title and content of each post.
"""

from modules import (
    sqlite3,  # A module for working with SQLite databases
    Blueprint,  # A class for creating Flask blueprints
    DB_POSTS_ROOT,  # A constant for the path to the posts database
    render_template,  # A function for rendering Jinja templates
)

indexBlueprint = Blueprint(
    "index", __name__
)  # Create a blueprint for the home page with the name "index" and the current module name


@indexBlueprint.route("/")  # Define a route for the home page
def index():
    """
    This function maps the home page route ("/") to the index function.

    It retrieves all posts from the database and passes them to the index.html.jinja template.

    The posts variable is passed to the index.html.jinja template as a list of dictionaries.

    The index.html.jinja template displays the title and content of each post.
    """
    connection = sqlite3.connect(DB_POSTS_ROOT)  # Connect to the posts database
    cursor = connection.cursor()  # Create a cursor object for executing queries
    cursor.execute(
        "select * from posts order by timeStamp desc"
    )  # Select all the columns from the posts table and order them by the timestamp in descending order
    posts = cursor.fetchall()  # Fetch all the results as a list of tuples
    return render_template(
        "index.html.jinja", posts=posts
    )  # Return the rendered template of the home page and pass the posts list as a keyword argument
