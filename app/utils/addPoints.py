import sqlite3
from constants import DB_USERS_ROOT
from utils.log import Log


# Function to add points to a user
def addPoints(points, user):
    """
    Adds the specified number of points to the user with the specified username.
    """
    Log.database(
        f"Connecting to '{DB_USERS_ROOT}' database"
    )  # Log the database connection is started
    connection = sqlite3.connect(DB_USERS_ROOT)  # Connect to the SQLite database
    connection.set_trace_callback(
        Log.database
    )  # Set the trace callback for the connection
    cursor = connection.cursor()  # Create a cursor object
    cursor.execute(  # Execute SQL query to update user points
        """update users set points = points+? where userName = ? """,
        [(points), (user)],
    )
    connection.commit()  # Commit changes to the database
    Log.info(f'{points} points added to "{user}"')
