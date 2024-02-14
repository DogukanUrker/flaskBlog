# Importing necessary modules
from modules import sqlite3, DB_USERS_ROOT, Log


# Function to get the profile picture of a user
def getProfilePicture(userName):
    """
    Returns the profile picture of the user with the specified username.

    Parameters:
        userName (str): The username of the user whose profile picture is to be retrieved.

    Returns:
        str or None: The profile picture URL of the user, or None if not found.
    """
    Log.sql(
        f"Connecting to '{DB_USERS_ROOT}' database"
    )  # Log the database connection is started
    # Connect to the SQLite database
    connection = sqlite3.connect(DB_USERS_ROOT)
    connection.set_trace_callback(Log.sql)  # Set the trace callback for the connection
    # Create a cursor object
    cursor = connection.cursor()
    # Execute SQL query to retrieve user profile picture
    cursor.execute(
        """select profilePicture from users where lower(userName) = ? """,
        [(userName.lower())],
    )
    try:
        # Fetch the profile picture URL
        profilePicture = cursor.fetchone()[0]
        # Log successful retrieval of profile picture
        Log.info(f"Returning {userName}'s profile picture: {profilePicture}")
    except:
        # If profile picture retrieval fails, set profilePicture to None and log danger message
        profilePicture = None
        Log.danger(f"Failed to retrieve profile picture for user: {userName}")

    return profilePicture  # Return the profile picture URL
