from modules import sqlite3, DB_USERS_ROOT, Log, session, redirect


# Function to change the role of a user
def changeUserRole(userName):
    """
    Changes the role of the user with the specified username.
    """
    userName = userName.lower()  # Convert username to lowercase
    Log.sql(
        f"Connecting to '{DB_USERS_ROOT}' database"
    )  # Log the database connection is started
    connection = sqlite3.connect(DB_USERS_ROOT)  # Connect to the SQLite database
    connection.set_trace_callback(Log.sql)  # Set the trace callback for the connection
    cursor = connection.cursor()  # Create a cursor object
    cursor.execute(  # Execute SQL query to retrieve user role
        """select role from users where lower(userName) = ? """,
        [(userName)],
    )
    role = cursor.fetchone()[0]  # Fetch the role value
    match role:
        case "admin":
            newRole = "user"
        case "user":
            newRole = "admin"
    cursor.execute(  # Execute SQL query to update user role
        """update users set role = ? where lower(userName) = ? """,
        [(newRole), (userName)],
    )
    Log.success(  # Log the role change event
        f'Admin: "{session["userName"]}" changed user: "{userName}"s role to "{newRole}" ',
    )
    connection.commit()  # Commit changes to the database
    match session["userName"].lower() == userName:
        case True:
            Log.success(f'Admin: "{session["userName"]}" changed his role to "user"')
            return redirect("/")
