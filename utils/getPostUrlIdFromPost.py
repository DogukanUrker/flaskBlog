# Importing necessary modules
from modules import DB_POSTS_ROOT, Log, sqlite3


# Function to get the urlID of posts using postID
def getPostUrlIdFromPost(postID: int):
    """
    Returns the post's urlID from post's id.
    Args:
        postID (int): The post's primary key/id whose urlID to be retrieved.

    Returns:
        str or None: The post's urlID of the post, or None if not found.
    """
    Log.sql(
        f"Connecting to '{DB_POSTS_ROOT}' database"
    )  # Log the database connection is started
    # Connect to the SQLite databse
    connection = sqlite3.connect(DB_POSTS_ROOT)
    connection.set_trace_callback(Log.sql)  # Set the trace callback for the connection
    # Create a cursor object
    cursor = connection.cursor()
    # Execute SQL query to retrieve user profile picture
    cursor.execute("""select urlID from posts where id = ?""", (postID,))
    try:
        # Fetch the post's urlID
        urlID = cursor.fetchone()[0]
        Log.info(f"Returning post's id {postID} and post's urlID: {urlID}")
    except:
        # If post's urlID retrieval fails, set urlID to None and log danger message
        urlID = None
        Log.danger(f"Failed to retrieve post's urlID for post id : {postID}")

    cursor.close()  # Close the database cursor
    connection.close()  # Close the database connection

    return urlID  # Return the post's urlID
