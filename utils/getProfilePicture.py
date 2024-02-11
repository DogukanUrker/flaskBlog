from modules import sqlite3, DB_USERS_ROOT, Log


# Function to get the profile picture of a user
def getProfilePicture(userName):
    """
    Returns the profile picture of the user with the specified username.
    """
    connection = sqlite3.connect(DB_USERS_ROOT)  # Connect to the SQLite database
    cursor = connection.cursor()  # Create a cursor object
    cursor.execute(  # Execute SQL query to retrieve user profile picture
        """select profilePicture from users where lower(userName) = ? """,
        [(userName.lower())],
    )
    profilePicture = cursor.fetchone()[0]  # Fetch the profile picture value

    # Log a message indicating that the user's profile picture is sending
    Log.info(f"Returning {userName}'s profile picture: {profilePicture}")

    # Return the profile picture
    return profilePicture
