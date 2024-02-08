from helpers import mkdir, exists, message, sqlite3


def dbFolder():
    match exists("db"):
        case True:
            message("6", 'Folder: "/db" FOUND')
        case False:
            message("1", 'Folder: "/db" NOT FOUND')
            mkdir("db")
            message("2", 'Folder: "/db" CREATED')


def usersTable():
    match exists("db/users.db"):
        case True:
            message("6", 'DATABASE: "users.db" FOUND')
        case False:
            message("1", 'DATABASE: "users.db" NOT FOUND')
            open("db/users.db", "x")
            message("2", 'DATABASE: "users.db" CREATED')
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT * FROM users; """).fetchall()
        message("6", 'TABLE: "Users" FOUND')
        connection.close()
    except:
        message("1", 'TABLE: "Users" NOT FOUND')
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
        message("2", 'TABLE: "Users" CREATED')


def postsTable():
    match exists("db/posts.db"):
        case True:
            message("6", 'DATABASE: "posts.db" FOUND')
        case False:
            message("1", 'DATABASE: "posts.db" NOT FOUND')
            open("db/posts.db", "x")
            message("2", 'DATABASE: "posts.db" CREATED')
    connection = sqlite3.connect("db/posts.db")
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT * FROM posts; """).fetchall()
        message("6", 'TABLE: "Posts" FOUND')
        connection.close()
    except:
        message("1", 'TABLE: "Posts" NOT FOUND')
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
        message("2", 'TABLE: "Posts" CREATED')


def commentsTable():
    match exists("db/comments.db"):
        case True:
            message("6", 'DATABASE: "comments.db" FOUND')
        case False:
            message("1", 'DATABASE: "comments.db" NOT FOUND')
            open("db/comments.db", "x")
            message("2", 'DATABASE: "comments.db" CREATED')
    connection = sqlite3.connect("db/comments.db")
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT * FROM comments; """).fetchall()
        message("6", 'TABLE: "Comments" FOUND')
        connection.close()
    except:
        message("1", 'TABLE: "Comments" NOT FOUND')
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
        message("2", 'TABLE: "Comments" CREATED')
