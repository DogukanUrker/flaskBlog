"""
This file contains the routes for the Flask application.

The Blueprint "index" is used to define the home page of the application.
The route "/" maps the index function to the home page.

The index function retrieves all posts from the database and passes them to the index.html.jinja template.

The posts variable is passed to the index.html.jinja template as a list of dictionaries.

The index.html.jinja template displays the title and content of each post.
"""

from helpers import (
    sqlite3,
    Blueprint,
    DB_POSTS_ROOT,
    render_template,
)

indexBlueprint = Blueprint("index", __name__)


@indexBlueprint.route("/")
def index():
    """
    This function maps the home page route ("/") to the index function.

    It retrieves all posts from the database and passes them to the index.html.jinja template.

    The posts variable is passed to the index.html.jinja template as a list of dictionaries.

    The index.html.jinja template displays the title and content of each post.
    """
    connection = sqlite3.connect(DB_POSTS_ROOT)
    cursor = connection.cursor()
    cursor.execute("select * from posts")
    posts = cursor.fetchall()
    return render_template("index.html.jinja", posts=posts)
