"""
This file contains the database schemas for the app.

The database consists of three tables:
1. Users: stores information about the users, including their username, email, password, profile picture, role, points, creation date, creation time, and verification status.
2. Posts: stores information about the posts, including their title, tags, content, author, date, time, views, last edit date, and last edit time.
3. Comments: stores information about the comments, including the post they are associated with, the comment text, the user who wrote the comment, the date, and the time.

This file contains functions to create the tables if they do not already exist, and to ensure that they have the correct structure.
"""

import sqlite3
from os.path import exists
from os import mkdir
from passlib.hash import sha512_crypt as encryption
from constants import (
    DB_ANALYTICS_ROOT,  # Root directory path for the analytics database
    DB_COMMENTS_ROOT,  # Root directory path for the comments database
    DB_FOLDER_ROOT,  # Root directory path for the database folder
    DB_POSTS_ROOT,  # Root directory path for the posts database
    DB_USERS_ROOT,  # Root directory path for the users database
    DEFAULT_ADMIN,  # Boolean indicating whether a default admin account should be created
    DEFAULT_ADMIN_EMAIL,  # Default email for the admin user
    DEFAULT_ADMIN_PASSWORD,  # Default password for the admin user
    DEFAULT_ADMIN_POINT,  # Default points assigned to the admin user
    DEFAULT_ADMIN_PROFILE_PICTURE,  # Default profile picture for the admin user
    DEFAULT_ADMIN_USERNAME,  # Default username for the admin user
)
from utils.log import Log
from utils.time import currentTimeStamp


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
            Log.info(f'Database folder: "/{DB_FOLDER_ROOT}" found')
        # If the path does not exist, print a message with the level 1 (alert) and the folder name
        case False:
            Log.error(f'Database folder: "/{DB_FOLDER_ROOT}" not found')
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
            Log.info(f'Users database: "{DB_USERS_ROOT}" found')
        # If the path does not exist, print a message with the level 1 (alert) and the database name
        case False:
            Log.error(f'Users database: "{DB_USERS_ROOT}" not found')
            # Use the open function with the "x" mode to create a new file for the database
            open(DB_USERS_ROOT, "x")
            # Print a message with the level 2 (success) and the database name
            Log.success(f'Users database: "{DB_USERS_ROOT}" created')
    Log.database(
        f"Connecting to '{DB_USERS_ROOT}' database"
    )  # Log the database connection is started
    # Use the sqlite3 module to connect to the database and get a cursor object
    connection = sqlite3.connect(DB_USERS_ROOT)
    connection.set_trace_callback(
        Log.database
    )  # Set the trace callback for the connection
    cursor = connection.cursor()
    try:
        # Try to execute a SQL query to select userID records from the users table
        cursor.execute("""select userID from users; """).fetchall()
        # If the query succeeds, print a message with the level 6 (informational) and the table name
        Log.info(f'Table: "users" found in "{DB_USERS_ROOT}"')
        # Close the connection to the database
        connection.close()
    except:
        # If the query fails, print a message with the level 1 (alert) and the table name
        Log.error(f'Table: "users" not found in "{DB_USERS_ROOT}"')
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
            Log.info(f'Posts database: "{DB_POSTS_ROOT}" found')
        # If the path does not exist, print a message with the level 1 (alert) and the database name
        case False:
            Log.error(f'Posts database: "{DB_POSTS_ROOT}" not found')
            # Use the open function with the "x" mode to create a new file for the database
            open(DB_POSTS_ROOT, "x")
            # Print a message with the level 2 (success) and the database name
            Log.success(f'Posts database: "{DB_POSTS_ROOT}" created')
    Log.database(
        f"Connecting to '{DB_POSTS_ROOT}' database"
    )  # Log the database connection is started
    # Use the sqlite3 module to connect to the database and get a cursor object
    connection = sqlite3.connect(DB_POSTS_ROOT)
    connection.set_trace_callback(
        Log.database
    )  # Set the trace callback for the connection
    cursor = connection.cursor()
    try:
        # Try to execute a SQL query to select id records from the posts table
        cursor.execute("""select id from posts; """).fetchall()
        # If the query succeeds, print a message with the level 6 (informational) and the table name
        Log.info(f'Table: "posts" found in "{DB_POSTS_ROOT}"')
        # Close the connection to the database
        connection.close()
    except:
        # If the query fails, print a message with the level 1 (alert) and the table name
        Log.error(f'Table: "posts" not found in "{DB_POSTS_ROOT}"')
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
            "urlID" TEXT NOT NULL,
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
            Log.info(f'Comments database: "{DB_COMMENTS_ROOT}" found')
        # If the path does not exist, print a message with the level 1 (alert) and the database name
        case False:
            Log.error(f'Comments database: "{DB_COMMENTS_ROOT}" not found')
            # Use the open function with the "x" mode to create a new file for the database
            open(DB_COMMENTS_ROOT, "x")
            # Print a message with the level 2 (success) and the database name
            Log.success(f'Comments database: "{DB_COMMENTS_ROOT}" created')
    Log.database(
        f"Connecting to '{DB_COMMENTS_ROOT}' database"
    )  # Log the database connection is started
    # Use the sqlite3 module to connect to the database and get a cursor object
    connection = sqlite3.connect(DB_COMMENTS_ROOT)
    connection.set_trace_callback(
        Log.database
    )  # Set the trace callback for the connection
    cursor = connection.cursor()
    try:
        # Try to execute a SQL query to select id records from the comments table
        cursor.execute("""select id from comments; """).fetchall()
        # If the query succeeds, print a message with the level 6 (informational) and the table name
        Log.info(f'Table: "comments" found in "{DB_COMMENTS_ROOT}"')
        # Close the connection to the database
        connection.close()
    except:
        # If the query fails, print a message with the level 1 (alert) and the table name
        Log.error(f'Table: "comments" not found in "{DB_COMMENTS_ROOT}"')
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


# This function checks if the analytics table exists in the database, and creates it if it does not.
def analyticsTable():
    """
    Checks if the analytics table exists in the database, and creates it if it does not.

    Returns:
        None
    """
    # Use the exists function to check if the DB_ANALYTICS_ROOT constant is a valid path
    match exists(DB_ANALYTICS_ROOT):
        # If the path exists, print a message with the level 6 (informational) and the database name
        case True:
            Log.info(f'Analytics database: "{DB_ANALYTICS_ROOT}" found')
        # If the path does not exist, print a message with the level 1 (alert) and the database name
        case False:
            Log.error(f'Analytics database: "{DB_ANALYTICS_ROOT}" not found')
            # Use the open function with the "x" mode to create a new file for the database
            open(DB_ANALYTICS_ROOT, "x")
            # Print a message with the level 2 (success) and the database name
            Log.success(f'Analytics database: "{DB_ANALYTICS_ROOT}" created')
    Log.database(
        f"Connecting to '{DB_ANALYTICS_ROOT}' database"
    )  # Log the database connection is started

    # Use the sqlite3 module to connect to the database and get a cursor object
    connection = sqlite3.connect(DB_ANALYTICS_ROOT)
    connection.set_trace_callback(
        Log.database
    )  # Set the trace callback for the connection
    cursor = connection.cursor()
    try:
        # Try to execute a SQL query to select id records from the postAnalytics table
        cursor.execute("""select id from postsAnalytics; """).fetchall()
        # If the query succeeds, print a message with the level 6 (informational) and the table name
        Log.info(f'Table: "postsAnalytics" found in "{DB_ANALYTICS_ROOT}"')
        # Close the connection to the database
        connection.close()
    except:
        # If the query fails, print a message with the level 1 (alert) and the table name
        Log.error(f'Table: "postsAnalytics" not found in "{DB_ANALYTICS_ROOT}"')
        # Define a SQL statement to create the postAnalytics table with the specified columns and constraints
        analyticsTable = """
        create table if not exists postsAnalytics(
            "id"    integer not null,
            "postID"  integer,
            "visitorUserName"  text,
            "country" text,
            "os" text,
            "continent" text,
            "timeSpendDuration" int default 0,
            "timeStamp" integer,
            primary key("id" autoincrement)
        );"""
        # Execute the SQL statement to create the table
        cursor.execute(analyticsTable)
        # Commit the changes to the database
        connection.commit()
        # Close the connection to the database
        connection.close()
        # Print a message with the level 2 (success) and the table name
        Log.success(f'Table: "postsAnalytics" created in "{DB_ANALYTICS_ROOT}"')
