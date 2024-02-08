from modules import sqlite3, DB_USERS_ROOT


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
    return cursor.fetchone()[0]  # Fetch the profile picture value
