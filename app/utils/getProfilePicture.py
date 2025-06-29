import sqlite3

from settings import DB_USERS_ROOT
from utils.log import Log


def getProfilePicture(userName):
    """
    Returns the profile picture of the user with the specified username.

    Parameters:
        userName (str): The username of the user whose profile picture is to be retrieved.

    Returns:
        str or None: The profile picture URL of the user, or None if not found.
    """
    Log.database(f"Connecting to '{DB_USERS_ROOT}' database")

    connection = sqlite3.connect(DB_USERS_ROOT)
    connection.set_trace_callback(Log.database)

    cursor = connection.cursor()

    cursor.execute(
        """select profilePicture from users where lower(userName) = ? """,
        [(userName.lower())],
    )
    try:
        profilePicture = cursor.fetchone()[0]

        Log.info(f"Returning {userName}'s profile picture: {profilePicture}")
    except Exception:
        profilePicture = None
        Log.error(f"Failed to retrieve profile picture for user: {userName}")

    return profilePicture
