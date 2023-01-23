import sqlite3
from app import message
from os.path import exists


def usersTable():
    if not exists("db/users.db"):
        message("1", '"users.db" NOT FOUND')
        open("db/users.db", "x")
        message("2", '"users.db" CREATED')
    else:
        message("2", '"users.db" FOUND')
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT * FROM users; """).fetchall()
        message("2", '"Users" TABLE FOUND')
        connection.close()
    except:
        message("1", '"Users" TABLE NOT FOUND')
        usersTable = """
        CREATE TABLE IF NOT EXISTS Users(
	    "userID"	INTEGER NOT NULL UNIQUE,
	    "userName"	TEXT UNIQUE,
	    "email"	TEXT UNIQUE,
	    "password"	TEXT,
	    "role"	TEXT,
	    "points"	INTEGER,
	    "creationDate"	TEXT,
	    "creationTime"	TEXT,
	    PRIMARY KEY("userID" AUTOINCREMENT)
        );"""

        cursor.execute(usersTable)
        connection.commit()
        connection.close()
        message("2", '"Users" TABLE CREATED')


def postsTable():
    if not exists("db/posts.db"):
        message("1", '"posts.db" NOT FOUND')
        open("db/posts.db", "x")
        message("2", '"posts.db" CREATED')
    else:
        message("2", '"posts.db" FOUND')
    connection = sqlite3.connect("db/posts.db")
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT * FROM posts; """).fetchall()
        message("2", '"Posts" TABLE FOUND')
        connection.close()
    except:
        message("1", '"Posts" TABLE NOT FOUND')
        postsTable = """
        CREATE TABLE IF NOT EXISTS posts(
	    "id"	INTEGER NOT NULL UNIQUE,
	    "title"	TEXT NOT NULL,
	    "tags"	TEXT,
	    "content"	TEXT NOT NULL,
	    "author"	TEXT NOT NULL,
	    "date"	BLOB NOT NULL,
	    "time"	BLOB NOT NULL,
	    "views"	TEXT,
	    PRIMARY KEY("id" AUTOINCREMENT)
        );"""

        cursor.execute(postsTable)
        connection.commit()
        connection.close()
        message("2", '"Posts" TABLE CREATED')


def commentsTable():
    if not exists("db/comments.db"):
        message("1", '"comments.db" NOT FOUND')
        open("db/comments.db", "x")
        message("2", '"comments.db" CREATED')
    else:
        message("2", '"comments.db" FOUND')
    connection = sqlite3.connect("db/comments.db")
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT * FROM comments; """).fetchall()
        message("2", '"Comments" TABLE FOUND')
        connection.close()
    except:
        message("1", '"Comments" TABLE NOT FOUND')
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
        message("2", '"Comments" TABLE CREATED')


usersTable()
postsTable()
commentsTable()
