"""
This file contains the database schemas for the app.

The database consists of three tables:
1. Users: stores information about the users, including their username, email, password, profile picture, role, points, creation date, creation time, and verification status.
2. Posts: stores information about the posts, including their title, tags, content, author, date, time, views, last edit date, and last edit time.
3. Comments: stores information about the comments, including the post they are associated with, the comment text, the user who wrote the comment, the date, and the time.

This file contains functions to create the tables if they do not already exist, and to ensure that they have the correct structure.
"""

from modules import mkdir, exists, Log, sqlite3, currentTimeStamp, encryption
from modules import (
    DB_USERS_ROOT,  # Root directory path for the users database
    DB_POSTS_ROOT,  # Root directory path for the posts database
    DEFAULT_ADMIN,  # Boolean indicating whether a default admin account should be created
    DB_FOLDER_ROOT,  # Root directory path for the database folder
    DB_COMMENTS_ROOT,  # Root directory path for the comments database
    DEFAULT_ADMIN_POINT,  # Default points assigned to the admin user
    DEFAULT_ADMIN_EMAIL,  # Default email for the admin user
    DEFAULT_ADMIN_USERNAME,  # Default username for the admin user
    DEFAULT_ADMIN_PASSWORD,  # Default password for the admin user
    DEFAULT_ADMIN_PROFILE_PICTURE,  # Default profile picture for the admin user
)


# This function checks if the database folder exists, and creates it if it does not.
def dbFolder():
    """
    Checks if the database folder exists, and create it if it does not.

    Returns:
        None
    """
    # Use the exists function to check if the DB_FOLDER_ROOT constant is a valid path
    match exists(DB_FOLDER_ROOT):
        # If the path exists, print a message with the level 6 (informational) and the folder name
        case True:
            Log.app(f'Database folder: "/{DB_FOLDER_ROOT}" found')
        # If the path does not exist, print a message with the level 1 (alert) and the folder name
        case False:
            Log.danger(f'Database folder: "/{DB_FOLDER_ROOT}" not found')
            # Use the mkdir function to create the folder
            mkdir(DB_FOLDER_ROOT)
            # Print a message with the level 2 (success) and the folder name
            Log.success(f'Database folder: "/{DB_FOLDER_ROOT}" created')


# This function checks if the users table exists in the database, and creates it if it does not.
def usersTable():
    """
    Checks if the users' table exists in the database, and create it if it does not.
    Checks if default admin is true create an admin user with custom admin account settings if it is.

    Returns:
        None
    """
    # Use the exists function to check if the DB_USERS_ROOT constant is a valid path
    match exists(DB_USERS_ROOT):
        # If the path exists, print a message with the level 6 (informational) and the database name
        case True:
            Log.app(f'Users database: "{DB_USERS_ROOT}" found')
        # If the path does not exist, print a message with the level 1 (alert) and the database name
        case False:
            Log.danger(f'Users database: "{DB_USERS_ROOT}" not found')
            # Use the open function with the "x" mode to create a new file for the database
            open(DB_USERS_ROOT, "x")
            # Print a message with the level 2 (success) and the database name
            Log.success(f'Users database: "{DB_USERS_ROOT}" created')
    Log.sql(
        f"Connecting to '{DB_USERS_ROOT}' database"
    )  # Log the database connection is started
    # Use the sqlite3 module to connect to the database and get a cursor object
    connection = sqlite3.connect(DB_USERS_ROOT)
    connection.set_trace_callback(Log.sql)  # Set the trace callback for the connection
    cursor = connection.cursor()
    try:
        # Try to execute a SQL query to select userID records from the users table
        cursor.execute("""select userID from users; """).fetchall()
        # If the query succeeds, print a message with the level 6 (informational) and the table name
        Log.app(f'Table: "users" found in "{DB_USERS_ROOT}"')
        # Close the connection to the database
        connection.close()
    except:
        # If the query fails, print a message with the level 1 (alert) and the table name
        Log.danger(f'Table: "users" not found in "{DB_USERS_ROOT}"')
        # Define a SQL statement to create the users table with the specified columns and constraints
        usersTable = """
        create table if not exists Users(
            "userID"    integer not null unique,
            "userName"  text unique,
            "email" text unique,
            "password"  text,
            "profilePicture" text,
            "role"  text,
            "points"    integer,
            "timeStamp" integer,
            "isVerified"    text,
            primary key("userID" autoincrement)
        );"""
        # Execute the SQL statement to create the table
        cursor.execute(usersTable)
        # Check if the DEFAULT_ADMIN constant is True
        match DEFAULT_ADMIN:
            # If True, create a default admin account with the specified values
            case True:
                # Hash the DEFAULT_ADMIN_PASSWORD using the encryption module
                password = encryption.hash(DEFAULT_ADMIN_PASSWORD)
                # Execute a SQL query to insert the default admin account into the users table
                cursor.execute(
                    """
                    insert into Users(userName,email,password,profilePicture,role,points,timeStamp,isVerified) \
                    values(?,?,?,?,?,?,?,?)
                    """,
                    (
                        DEFAULT_ADMIN_USERNAME,
                        DEFAULT_ADMIN_EMAIL,
                        password,
                        DEFAULT_ADMIN_PROFILE_PICTURE,
                        "admin",
                        DEFAULT_ADMIN_POINT,
                        currentTimeStamp(),
                        "True",
                    ),
                )
                # Commit the changes to the database
                connection.commit()
                # Print a message with the level 2 (success) and the default admin username
                Log.success(
                    f'Admin: "{DEFAULT_ADMIN_USERNAME}" added to database as initial admin',
                )
        # Commit the changes to the database
        connection.commit()
        # Close the connection to the database
        connection.close()
        # Print a message with the level 2 (success) and the table name
        Log.success(f'Table: "users" created in "{DB_USERS_ROOT}"')


# This function checks if the posts table exists in the database, and creates it if it does not.
def postsTable():
    """
    Checks if the posts table exists in the database, and creates it if it does not.

    Returns:
        None
    """
    # Use the exists function to check if the DB_POSTS_ROOT constant is a valid path
    match exists(DB_POSTS_ROOT):
        # If the path exists, print a message with the level 6 (informational) and the database name
        case True:
            Log.app(f'Posts database: "{DB_POSTS_ROOT}" found')
        # If the path does not exist, print a message with the level 1 (alert) and the database name
        case False:
            Log.danger(f'Posts database: "{DB_POSTS_ROOT}" not found')
            # Use the open function with the "x" mode to create a new file for the database
            open(DB_POSTS_ROOT, "x")
            # Print a message with the level 2 (success) and the database name
            Log.success(f'Posts database: "{DB_POSTS_ROOT}" created')
    Log.sql(
        f"Connecting to '{DB_POSTS_ROOT}' database"
    )  # Log the database connection is started
    # Use the sqlite3 module to connect to the database and get a cursor object
    connection = sqlite3.connect(DB_POSTS_ROOT)
    connection.set_trace_callback(Log.sql)  # Set the trace callback for the connection
    cursor = connection.cursor()
    try:
        # Try to execute a SQL query to select id records from the posts table
        cursor.execute("""select id from posts; """).fetchall()
        # If the query succeeds, print a message with the level 6 (informational) and the table name
        Log.app(f'Table: "posts" found in "{DB_POSTS_ROOT}"')
        # Close the connection to the database
        connection.close()
    except:
        # If the query fails, print a message with the level 1 (alert) and the table name
        Log.danger(f'Table: "posts" not found in "{DB_POSTS_ROOT}"')
        # Define a SQL statement to create the posts table with the specified columns and constraints
        postsTable = """
        CREATE TABLE "posts" (
            "id"    integer not null unique,
            "title" text not null,
            "tags"  text not null,
            "content"   text not null,
            "banner"    BLOB not null,
            "author"    text not null,
            "views" integer,
            "timeStamp" integer,
            "lastEditTimeStamp" integer,
            "category"  text not null,
            primary key("id" autoincrement)
        );"""
        # Execute the SQL statement to create the table
        cursor.execute(postsTable)
        # Commit the changes to the database
        connection.commit()
        # Close the connection to the database
        connection.close()
        # Print a message with the level 2 (success) and the table name
        Log.success(f'Table: "posts" created in "{DB_POSTS_ROOT}"')


# This function checks if the comments table exists in the database, and creates it if it does not.
def commentsTable():
    """
    Checks if the comments table exists in the database, and creates it if it does not.

    Returns:
        None
    """
    # Use the exists function to check if the DB_COMMENTS_ROOT constant is a valid path
    match exists(DB_COMMENTS_ROOT):
        # If the path exists, print a message with the level 6 (informational) and the database name
        case True:
            Log.app(f'Comments database: "{DB_COMMENTS_ROOT}" found')
        # If the path does not exist, print a message with the level 1 (alert) and the database name
        case False:
            Log.danger(f'Comments database: "{DB_COMMENTS_ROOT}" not found')
            # Use the open function with the "x" mode to create a new file for the database
            open(DB_COMMENTS_ROOT, "x")
            # Print a message with the level 2 (success) and the database name
            Log.success(f'Comments database: "{DB_COMMENTS_ROOT}" created')
    Log.sql(
        f"Connecting to '{DB_COMMENTS_ROOT}' database"
    )  # Log the database connection is started
    # Use the sqlite3 module to connect to the database and get a cursor object
    connection = sqlite3.connect(DB_COMMENTS_ROOT)
    connection.set_trace_callback(Log.sql)  # Set the trace callback for the connection
    cursor = connection.cursor()
    try:
        # Try to execute a SQL query to select id records from the comments table
        cursor.execute("""select id from comments; """).fetchall()
        # If the query succeeds, print a message with the level 6 (informational) and the table name
        Log.app(f'Table: "comments" found in "{DB_COMMENTS_ROOT}"')
        # Close the connection to the database
        connection.close()
    except:
        # If the query fails, print a message with the level 1 (alert) and the table name
        Log.danger(f'Table: "comments" not found in "{DB_COMMENTS_ROOT}"')
        # Define a SQL statement to create the comments table with the specified columns and constraints
        commentsTable = """
        create table if not exists comments(
            "id"    integer not null,
            "post"  integer,
            "comment"   text,
            "user"  text,
            "timeStamp" integer,
            primary key("id" autoincrement)
        );"""
        # Execute the SQL statement to create the table
        cursor.execute(commentsTable)
        # Commit the changes to the database
        connection.commit()
        # Close the connection to the database
        connection.close()
        # Print a message with the level 2 (success) and the table name
        Log.success(f'Table: "comments" created in "{DB_COMMENTS_ROOT}"')
