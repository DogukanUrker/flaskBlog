"""
This file contains the database schemas for the app.

The database consists of three tables:
1. Users: stores information about the users, including their username, email, password, profile picture, role, points, creation date, creation time, and verification status.
2. Posts: stores information about the posts, including their title, tags, content, author, date, time, views, last edit date, and last edit time.
3. Comments: stores information about the comments, including the post they are associated with, the comment text, the user who wrote the comment, the date, and the time.

This file contains functions to create the tables if they do not already exist, and to ensure that they have the correct structure.
"""

import sqlite3
from os import mkdir
from os.path import exists

from passlib.hash import sha512_crypt as encryption
from settings import (
    DB_ANALYTICS_ROOT,
    DB_COMMENTS_ROOT,
    DB_FOLDER_ROOT,
    DB_POSTS_ROOT,
    DB_USERS_ROOT,
    DEFAULT_ADMIN,
    DEFAULT_ADMIN_EMAIL,
    DEFAULT_ADMIN_PASSWORD,
    DEFAULT_ADMIN_POINT,
    DEFAULT_ADMIN_PROFILE_PICTURE,
    DEFAULT_ADMIN_USERNAME,
)
from utils.log import Log
from utils.time import currentTimeStamp


def dbFolder():
    """
    Checks if the database folder exists, and create it if it does not.

    Returns:
        None
    """

    match exists(DB_FOLDER_ROOT):
        case True:
            Log.info(f'Database folder: "/{DB_FOLDER_ROOT}" found')

        case False:
            Log.error(f'Database folder: "/{DB_FOLDER_ROOT}" not found')

            mkdir(DB_FOLDER_ROOT)

            Log.success(f'Database folder: "/{DB_FOLDER_ROOT}" created')


def usersTable():
    """
    Checks if the users' table exists in the database, and create it if it does not.
    Checks if default admin is true create an admin user with custom admin account settings if it is.

    Returns:
        None
    """

    match exists(DB_USERS_ROOT):
        case True:
            Log.info(f'Users database: "{DB_USERS_ROOT}" found')

        case False:
            Log.error(f'Users database: "{DB_USERS_ROOT}" not found')

            open(DB_USERS_ROOT, "x")

            Log.success(f'Users database: "{DB_USERS_ROOT}" created')
    Log.database(f"Connecting to '{DB_USERS_ROOT}' database")

    connection = sqlite3.connect(DB_USERS_ROOT)
    connection.set_trace_callback(Log.database)
    cursor = connection.cursor()
    try:
        cursor.execute("""select userID from users; """).fetchall()

        Log.info(f'Table: "users" found in "{DB_USERS_ROOT}"')

        connection.close()
    except Exception:
        Log.error(f'Table: "users" not found in "{DB_USERS_ROOT}"')

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

        cursor.execute(usersTable)

        match DEFAULT_ADMIN:
            case True:
                password = encryption.hash(DEFAULT_ADMIN_PASSWORD)

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

                connection.commit()

                Log.success(
                    f'Admin: "{DEFAULT_ADMIN_USERNAME}" added to database as initial admin',
                )

        connection.commit()

        connection.close()

        Log.success(f'Table: "users" created in "{DB_USERS_ROOT}"')


def postsTable():
    """
    Checks if the posts table exists in the database, and creates it if it does not.

    Returns:
        None
    """

    match exists(DB_POSTS_ROOT):
        case True:
            Log.info(f'Posts database: "{DB_POSTS_ROOT}" found')

        case False:
            Log.error(f'Posts database: "{DB_POSTS_ROOT}" not found')

            open(DB_POSTS_ROOT, "x")

            Log.success(f'Posts database: "{DB_POSTS_ROOT}" created')
    Log.database(f"Connecting to '{DB_POSTS_ROOT}' database")

    connection = sqlite3.connect(DB_POSTS_ROOT)
    connection.set_trace_callback(Log.database)
    cursor = connection.cursor()
    try:
        cursor.execute("""select id from posts; """).fetchall()

        Log.info(f'Table: "posts" found in "{DB_POSTS_ROOT}"')

        connection.close()
    except Exception:
        Log.error(f'Table: "posts" not found in "{DB_POSTS_ROOT}"')

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

        cursor.execute(postsTable)

        connection.commit()

        connection.close()

        Log.success(f'Table: "posts" created in "{DB_POSTS_ROOT}"')


def commentsTable():
    """
    Checks if the comments table exists in the database, and creates it if it does not.

    Returns:
        None
    """

    match exists(DB_COMMENTS_ROOT):
        case True:
            Log.info(f'Comments database: "{DB_COMMENTS_ROOT}" found')

        case False:
            Log.error(f'Comments database: "{DB_COMMENTS_ROOT}" not found')

            open(DB_COMMENTS_ROOT, "x")

            Log.success(f'Comments database: "{DB_COMMENTS_ROOT}" created')
    Log.database(f"Connecting to '{DB_COMMENTS_ROOT}' database")

    connection = sqlite3.connect(DB_COMMENTS_ROOT)
    connection.set_trace_callback(Log.database)
    cursor = connection.cursor()
    try:
        cursor.execute("""select id from comments; """).fetchall()

        Log.info(f'Table: "comments" found in "{DB_COMMENTS_ROOT}"')

        connection.close()
    except Exception:
        Log.error(f'Table: "comments" not found in "{DB_COMMENTS_ROOT}"')

        commentsTable = """
        create table if not exists comments(
            "id"    integer not null,
            "post"  integer,
            "comment"   text,
            "user"  text,
            "timeStamp" integer,
            primary key("id" autoincrement)
        );"""

        cursor.execute(commentsTable)

        connection.commit()

        connection.close()

        Log.success(f'Table: "comments" created in "{DB_COMMENTS_ROOT}"')


def analyticsTable():
    """
    Checks if the analytics table exists in the database, and creates it if it does not.

    Returns:
        None
    """

    match exists(DB_ANALYTICS_ROOT):
        case True:
            Log.info(f'Analytics database: "{DB_ANALYTICS_ROOT}" found')

        case False:
            Log.error(f'Analytics database: "{DB_ANALYTICS_ROOT}" not found')

            open(DB_ANALYTICS_ROOT, "x")

            Log.success(f'Analytics database: "{DB_ANALYTICS_ROOT}" created')
    Log.database(f"Connecting to '{DB_ANALYTICS_ROOT}' database")

    connection = sqlite3.connect(DB_ANALYTICS_ROOT)
    connection.set_trace_callback(Log.database)
    cursor = connection.cursor()
    try:
        cursor.execute("""select id from postsAnalytics; """).fetchall()

        Log.info(f'Table: "postsAnalytics" found in "{DB_ANALYTICS_ROOT}"')

        connection.close()
    except Exception:
        Log.error(f'Table: "postsAnalytics" not found in "{DB_ANALYTICS_ROOT}"')

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

        cursor.execute(analyticsTable)

        connection.commit()

        connection.close()

        Log.success(f'Table: "postsAnalytics" created in "{DB_ANALYTICS_ROOT}"')
