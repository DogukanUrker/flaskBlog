import sqlite3

from settings import Settings
from utils.log import Log


def get_profile_picture(user_name):
    """
    Returns the profile picture of the user with the specified username.

    Parameters:
        user_name (str): The username of the user whose profile picture is to be retrieved.

    Returns:
        str or None: The profile picture URL of the user, or None if not found.
    """
    Log.database(f"Connecting to '{Settings.DB_USERS_ROOT}' database")

    connection = sqlite3.connect(Settings.DB_USERS_ROOT)
    connection.set_trace_callback(Log.database)

    cursor = connection.cursor()

    cursor.execute(
        """select profile_picture from users where lower(user_name) = ? """,
        [(user_name.lower())],
    )
    try:
        profile_picture = cursor.fetchone()[0]

        Log.info(f"Returning {user_name}'s profile picture: {profile_picture}")
    except Exception:
        profile_picture = None
        Log.error(f"Failed to retrieve profile picture for user: {user_name}")

    return profile_picture
