"""
This file contains the code for the category page.

The category page displays a list of all the posts in a specific category.
It is accessible through the /category/<category> URL.

The code in this file is organized as follows:

1. Import statements: The necessary modules are imported.

2. Category blueprint: A blueprint for the category page is defined.

3. category route: The category route is defined, which takes a category
   parameter. The route checks if the specified category exists, and if not,
   returns a 404 error.

4. The posts are retrieved from the database and rendered as HTML.

"""

from helpers import (
    abort,
    sqlite3,
    Blueprint,
    DB_POSTS_ROOT,
    render_template,
)

categoryBlueprint = Blueprint("category", __name__)


@categoryBlueprint.route("/category/<category>")
def category(category):
    """
    This function returns the category page.

    Args:
        category (str): The category name.

    Returns:
        The category page as a template.

    Raises:
        404: If the specified category does not exist.
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
    match category.lower() in categories:
        case False:
            abort(404)
    connection = sqlite3.connect(DB_POSTS_ROOT)
    cursor = connection.cursor()
    cursor.execute(
        """select * from posts where lower(category) = ? order by timeStamp desc""",
        [(category.lower())],
    )
    posts = cursor.fetchall()
    return render_template("category.html.jinja", posts=posts, category=category)
