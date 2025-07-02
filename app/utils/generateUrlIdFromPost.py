import sqlite3
import uuid

from settings import DB_POSTS_ROOT
from utils.log import Log


def checkIfurlIDExistsInPostDb(urlID):
    with sqlite3.connect(DB_POSTS_ROOT) as connection:
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()
        cursor.execute("SELECT urlID FROM posts WHERE urlID = ?", (urlID,))
        return bool(cursor.fetchall())


AVOID_CHARACTERS = [
    " ",
    "<",
    ">",
    "#",
    "%",
    "{",
    "}",
    "|",
    "\\",
    "^",
    "~",
    "[",
    "]",
    "`",
    '"',
    "'",
    ":",
    ";",
    "/",
    "?",
    "=",
    "&",
    "@",
    "+",
    ".",
    ",",
]


def getNewUid():
    return str(uuid.uuid4())[24:]


def getSlugFromPostTitle(postTitle):
    cleanedTitle = "".join(
        ["-" if char in AVOID_CHARACTERS else char for char in postTitle]
    )
    filteredWords = [word for word in cleanedTitle.split("-") if word]
    finalUrl = "-".join(filteredWords)
    return f"{finalUrl}".lower()


def generateurlID():
    newurlID = getNewUid()
    counter = 1

    while checkIfurlIDExistsInPostDb(newurlID):
        newurlID = f"{newurlID}{counter}"
        counter += 1

    return newurlID
