# Import the necessary modules and functions
from helpers import (
    sqlite3,
    Blueprint,
    DB_POSTS_ROOT,
    DB_USERS_ROOT,
    render_template,
)

# Create a blueprint for the search route
searchBlueprint = Blueprint("search", __name__)


@searchBlueprint.route("/search/<query>", methods=["GET", "POST"])
def search(query):
    # Replace the %20 and + characters in the query with spaces
    query = query.replace("%20", " ")
    queryNoWhiteSpace = query.replace("+", "")
    query = query.replace("+", " ")
    # Connect to the users database
    connection = sqlite3.connect(DB_USERS_ROOT)
    cursor = connection.cursor()
    # Search for users whose user name contains the query
    queryUsers = cursor.execute(
        """select * from users where userName like ? """,
        [
            ("%" + query + "%"),
        ],
    ).fetchall()
    # Search for users whose user name contains the query without spaces
    queryUsers = cursor.execute(
        """select * from users where userName like ? """,
        [
            ("%" + queryNoWhiteSpace + "%"),
        ],
    ).fetchall()
    # Connect to the posts database
    connection = sqlite3.connect(DB_POSTS_ROOT)
    cursor = connection.cursor()
    # Search for posts whose tags contain the query
    queryTags = cursor.execute(
        """select * from posts where tags like ? """,
        [
            ("%" + query + "%"),
        ],
    ).fetchall()
    # Search for posts whose title contains the query
    queryTitles = cursor.execute(
        """select * from posts where title like ? """,
        [
            ("%" + query + "%"),
        ],
    ).fetchall()
    # Search for posts whose author contains the query
    queryAuthors = cursor.execute(
        """select * from posts where author like ? """,
        [
            ("%" + query + "%"),
        ],
    ).fetchall()
    # Search for posts whose tags contain the query without spaces
    queryTags = cursor.execute(
        """select * from posts where tags like ? """,
        [
            ("%" + queryNoWhiteSpace + "%"),
        ],
    ).fetchall()
    # Search for posts whose title contains the query without spaces
    queryTitles = cursor.execute(
        """select * from posts where title like ? """,
        [
            ("%" + queryNoWhiteSpace + "%"),
        ],
    ).fetchall()
    # Search for posts whose author contains the query without spaces
    queryAuthors = cursor.execute(
        """select * from posts where author like ? """,
        [
            ("%" + queryNoWhiteSpace + "%"),
        ],
    ).fetchall()
    # Initialize an empty list for posts
    posts = []
    # Initialize an empty list for users
    users = []
    # Initialize a flag for empty results
    empty = False
    # Check if any posts match the query by tags
    match queryTags == []:
        case False:
            # Append the matching posts to the posts list
            posts.append(queryTags)
    # Check if any posts match the query by title
    match queryTitles == []:
        case False:
            # Append the matching posts to the posts list
            posts.append(queryTitles)
    # Check if any posts match the query by author
    match queryAuthors == []:
        case False:
            # Append the matching posts to the posts list
            posts.append(queryAuthors)
    # Check if any users match the query by user name
    match queryUsers == []:
        case False:
            # Append the matching users to the users list
            users.append(queryUsers)
    # Check if both posts and users lists are empty
    match not posts and not users:
        case True:
            # Set the empty flag to True
            empty = True
    # Initialize an empty list for results ID
    resultsID = []
    # Loop through the posts list
    for post in posts:
        # Loop through each post in the sub-list
        for post in post:
            # Check if the post ID is not already in the results ID list
            match post[0] not in resultsID:
                case True:
                    # Append the post ID to the results ID list
                    resultsID.append(post[0])
    # Reinitialize the posts list as empty
    posts = []
    # Loop through the results ID list
    for postID in resultsID:
        # Query the posts database for the post with the matching ID
        cursor.execute(
            """select * from posts where id = ? """,
            [(postID)],
        )
        # Append the post to the posts list
        posts.append(cursor.fetchall())
    # Render the search template with the posts, users, query and empty data
    return render_template(
        "search.html",
        posts=posts,
        users=users,
        query=query,
        empty=empty,
    )
