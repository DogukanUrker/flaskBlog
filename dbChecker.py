"""
This file contains the database schemas for the app.

The database consists of three tables:
1. Users: stores information about the users, including their username, email, password, profile picture, role, points, creation date, creation time, and verification status.
2. Posts: stores information about the posts, including their title, tags, content, author, date, time, views, last edit date, and last edit time.
3. Comments: stores information about the comments, including the post they are associated with, the comment text, the user who wrote the comment, the date, and the time.

This file contains functions to create the tables if they do not already exist, and to ensure that they have the correct structure.
"""

from helpers import mkdir, exists, message, sqlite3, currentTimeStamp, sha256_crypt
from constants import (
    DB_USERS_ROOT,
    DB_POSTS_ROOT,
    DEFAULT_ADMIN,
    DB_FOLDER_ROOT,
    DB_COMMENTS_ROOT,
    DEFAULT_ADMIN_POINT,
    DEFAULT_ADMIN_EMAIL,
    DEFAULT_ADMIN_USERNAME,
    DEFAULT_ADMIN_PASSWORD,
    DEFAULT_ADMIN_PROFILE_PICTURE,
)


def dbFolder():
    """
    Checks if the database folder exists, and creates it if it does not.

    Returns:
        None
    """
    match exists(DB_FOLDER_ROOT):
        case True:
            message("6", f'DATABASE FOLDER: "/{DB_FOLDER_ROOT}" FOUND')
        case False:
            message("1", f'DATABASE FOLDER: "/{DB_FOLDER_ROOT}" NOT FOUND')
            mkdir(DB_FOLDER_ROOT)
            message("2", f'DATABASE FOLDER: "/{DB_FOLDER_ROOT}" CREATED')


def usersTable():
    """
    Checks if the users table exists in the database, and creates it if it does not.

    Returns:
        None
    """
    match exists(DB_USERS_ROOT):
        case True:
            message("6", f'USERS DATABASE: "{DB_USERS_ROOT}" FOUND')
        case False:
            message("1", f'USERS DATABASE: "{DB_USERS_ROOT}" NOT FOUND')
            open(DB_USERS_ROOT, "x")
            message("2", f'USERS DATABASE: "{DB_USERS_ROOT}" CREATED')
    connection = sqlite3.connect(DB_USERS_ROOT)
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT * FROM users; """).fetchall()
        message("6", f'TABLE: "Users" FOUND IN "{DB_USERS_ROOT}"')
        connection.close()
    except:
        message("1", f'TABLE: "Users" NOT FOUND IN "{DB_USERS_ROOT}"')
        usersTable = """
        CREATE TABLE IF NOT EXISTS Users(
            "userID"	INTEGER NOT NULL UNIQUE,
            "userName"	TEXT UNIQUE,
            "email"	TEXT UNIQUE,
            "password"	TEXT,
            "profilePicture" TEXT,
            "role"	TEXT,
            "points"	INTEGER,
            "timeStamp"	INTEGER,
            "isVerified"	TEXT,
            PRIMARY KEY("userID" AUTOINCREMENT)
        );"""
        cursor.execute(usersTable)
        match DEFAULT_ADMIN:
            case True:
                password = sha256_crypt.hash(DEFAULT_ADMIN_PASSWORD)
                cursor.execute(
                    """
                    INSERT INTO Users(userName,email,password,profilePicture,role,points,timeStamp,isVerified) \
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
                connection.commit()
                message(
                    "2",
                    f'ADMIN: "{DEFAULT_ADMIN_USERNAME}" ADDED TO DATABASE AS INITIAL ADMIN',
                )
        connection.commit()
        connection.close()
        message("2", f'TABLE: "Users" CREATED IN "{DB_USERS_ROOT}"')


def postsTable():
    """
    Checks if the posts table exists in the database, and creates it if it does not.

    Returns:
        None
    """
    match exists(DB_POSTS_ROOT):
        case True:
            message("6", f'POSTS DATABASE: "{DB_POSTS_ROOT}" FOUND')
        case False:
            message("1", f'POSTS DATABASE: "{DB_POSTS_ROOT}" NOT FOUND')
            open(DB_POSTS_ROOT, "x")
            message("2", f'POSTS DATABASE: "{DB_POSTS_ROOT}" CREATED')
    connection = sqlite3.connect(DB_POSTS_ROOT)
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT * FROM posts; """).fetchall()
        message("6", f'TABLE: "Posts" FOUND IN "{DB_POSTS_ROOT}"')
        connection.close()
    except:
        message("1", f'TABLE: "Posts" NOT FOUND IN "{DB_POSTS_ROOT}"')
        postsTable = """
        CREATE TABLE "posts" (
            "id"	INTEGER NOT NULL UNIQUE,
            "title"	TEXT NOT NULL,
            "tags"	TEXT,
            "content"	TEXT NOT NULL,
            "author"	TEXT NOT NULL,
            "views"	TEXT,
            "timeStamp"	INTEGER,
            "lastEditTimeStamp"	INTEGER,
            PRIMARY KEY("id" AUTOINCREMENT)
        );"""
        cursor.execute(postsTable)
        connection.commit()
        connection.close()
        message("2", f'TABLE: "Posts" CREATED IN "{DB_POSTS_ROOT}"')


def commentsTable():
    """
    Checks if the comments table exists in the database, and creates it if it does not.

    Returns:
        None
    """
    match exists(DB_COMMENTS_ROOT):
        case True:
            message("6", f'COMMENTS DATABASE: "{DB_COMMENTS_ROOT}" FOUND')
        case False:
            message("1", f'COMMENTS DATABASE: "{DB_COMMENTS_ROOT}" NOT FOUND')
            open(DB_COMMENTS_ROOT, "x")
            message("2", f'COMMENTS DATABASE: "{DB_COMMENTS_ROOT}" CREATED')
    connection = sqlite3.connect(DB_COMMENTS_ROOT)
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT * FROM comments; """).fetchall()
        message("6", f'TABLE: "Comments" FOUND IN "{DB_COMMENTS_ROOT}"')
        connection.close()
    except:
        message("1", f'TABLE: "Comments" NOT FOUND IN "{DB_COMMENTS_ROOT}"')
        commentsTable = """
        CREATE TABLE IF NOT EXISTS comments(
            "id"	INTEGER NOT NULL,
            "post"	INTEGER,
            "comment"	TEXT,
            "user"	TEXT,
            "timeStamp"	INTEGER,
            PRIMARY KEY("id" AUTOINCREMENT)
        );"""
        cursor.execute(commentsTable)
        connection.commit()
        connection.close()
        message("2", f'TABLE: "Comments" CREATED IN "{DB_COMMENTS_ROOT}"')
