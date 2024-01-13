from helpers import mkdir, exists, message, sqlite3
from constants import DB_FOLDER_ROOT, DB_USERS_ROOT, DB_POSTS_ROOT, DB_COMMENTS_ROOT


def dbFolder():
    match exists(DB_FOLDER_ROOT):
        case True:
            message("6", f'DATABASE FOLDER: "/{DB_FOLDER_ROOT}" FOUND')
        case False:
            message("1", f'DATABASE FOLDER: "/{DB_FOLDER_ROOT}" NOT FOUND')
            mkdir(DB_FOLDER_ROOT)
            message("2", f'DATABASE FOLDER: "/{DB_FOLDER_ROOT}" CREATED')


def usersTable():
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
	    "creationDate"	TEXT,
	    "creationTime"	TEXT,
        "isVerified"	TEXT,
	    PRIMARY KEY("userID" AUTOINCREMENT)
        );"""
        cursor.execute(usersTable)
        connection.commit()
        connection.close()
        message("2", f'TABLE: "Users" CREATED IN "{DB_USERS_ROOT}"')


def postsTable():
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
    	"date"	TEXT NOT NULL,
    	"time"	TEXT NOT NULL,
    	"views"	TEXT,
    	"lastEditDate"	TEXT,
        "lastEditTime"	TEXT,
    	PRIMARY KEY("id" AUTOINCREMENT)
        );"""
        cursor.execute(postsTable)
        connection.commit()
        connection.close()
        message("2", f'TABLE: "Posts" CREATED IN "{DB_POSTS_ROOT}"')


def commentsTable():
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
	    "date"	TEXT,
	    "time"	TEXT,
	    PRIMARY KEY("id" AUTOINCREMENT)
        );"""
        cursor.execute(commentsTable)
        connection.commit()
        connection.close()
        message("2", f'TABLE: "Comments" CREATED IN "{DB_COMMENTS_ROOT}"')
