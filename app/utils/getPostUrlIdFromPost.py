import sqlite3

from settings import Settings
from utils.log import Log


def getPostUrlIdFromPost(postID: int):
    """
    Returns the post's urlID from post's id.
    Args:
        postID (int): The post's primary key/id whose urlID to be retrieved.

    Returns:
        str or None: The post's urlID of the post, or None if not found.
    """
    Log.database(f"Connecting to '{Settings.DB_POSTS_ROOT}' database")

    connection = sqlite3.connect(Settings.DB_POSTS_ROOT)
    connection.set_trace_callback(Log.database)

    cursor = connection.cursor()

    cursor.execute("""select urlID from posts where id = ?""", (postID,))
    try:
        urlID = cursor.fetchone()[0]
        Log.info(f"Returning post's id {postID} and post's urlID: {urlID}")
    except Exception:
        urlID = None
        Log.error(f"Failed to retrieve post's urlID for post id : {postID}")

    cursor.close()
    connection.close()

    return urlID
