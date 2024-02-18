# Import necessary modules and functions
from modules import (
    Log,  # Logging module
    sqlite3,  # Module for interacting with SQLite databases
    Blueprint,  # Class for defining Flask blueprints, which are sets of routes
    DB_POSTS_ROOT,  # Variable containing the path to the posts database
    DB_USERS_ROOT,  # Variable containing the path to the users database
    render_template,  # Function for rendering HTML templates
)

# Create a blueprint for the search route
searchBlueprint = Blueprint("search", __name__)


# Define the route handler for the search page
@searchBlueprint.route("/search/<query>", methods=["GET", "POST"])
def search(query):
    # Replace the %20 and + characters in the query with spaces
    query = query.replace("%20", " ")
    queryNoWhiteSpace = query.replace("+", "")
    query = query.replace("+", " ")

    # Log the query
    Log.info(f"Searching for query: {query}")

    Log.sql(
        f"Connecting to '{DB_USERS_ROOT}' database"
    )  # Log the database connection is started

    # Connect to the users database
    connection = sqlite3.connect(DB_USERS_ROOT)
    connection.set_trace_callback(Log.sql)  # Set the trace callback for the connection
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
    Log.sql(
        f"Connecting to '{DB_POSTS_ROOT}' database"
    )  # Log the database connection is started
    # Connect to the posts database
    connection = sqlite3.connect(DB_POSTS_ROOT)
    connection.set_trace_callback(Log.sql)  # Set the trace callback for the connection
    cursor = connection.cursor()

    # Search for posts whose tags contain the query
    queryTags = cursor.execute(
        """select * from posts where tags like ? order by timeStamp desc""",
        [
            ("%" + query + "%"),
        ],
    ).fetchall()

    # Search for posts whose title contains the query
    queryTitles = cursor.execute(
        """select * from posts where title like ? order by timeStamp desc""",
        [
            ("%" + query + "%"),
        ],
    ).fetchall()

    # Search for posts whose author contains the query
    queryAuthors = cursor.execute(
        """select * from posts where author like ? order by timeStamp desc""",
        [
            ("%" + query + "%"),
        ],
    ).fetchall()

    # Search for posts whose tags contain the query without spaces
    queryTags = cursor.execute(
        """select * from posts where tags like ? order by timeStamp desc""",
        [
            ("%" + queryNoWhiteSpace + "%"),
        ],
    ).fetchall()

    # Search for posts whose title contains the query without spaces
    queryTitles = cursor.execute(
        """select * from posts where title like ? order by timeStamp desc""",
        [
            ("%" + queryNoWhiteSpace + "%"),
        ],
    ).fetchall()

    # Search for posts whose author contains the query without spaces
    queryAuthors = cursor.execute(
        """select * from posts where author like ? order by timeStamp desc""",
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

    # Use the Log module to log information to the console
    Log.info(
        f"Rendering search.html.jinja: params: query={query} | users={users} | posts={len(posts)} | empty={empty}"
    )

    # Render the search template with the posts, users, query and empty data
    return render_template(
        "search.html.jinja",
        posts=posts,
        users=users,
        query=query,
        empty=empty,
    )
