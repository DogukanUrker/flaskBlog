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
    "\\",  # Backslash
    "^",  # Caret
    "~",  # Tilde
    "[",  # Square brackets
    "]",  # Square brackets
    "`",  # Backtick
    '"',  # Double quote
    "'",  # Single quote
    ":",  # Colon
    ";",  # Semicolon
    "/",  # Slash
    "?",  # Question mark
    "=",  # Equals
    "&",  # Ampersand
    "@",  # At
    "+",  # Plus
    ".",  # Period
    ",",  # Comma
]  # Characters to avoid in post title for URL Slug generation function to work properly. Add more characters if needed.


# Function to generate a new unique ID
def getNewUid():
    return str(uuid.uuid4())[24:]


# Function to convert post title to URL SLUG
def getSlugFromPostTitle(postTitle):
    cleanedTitle = "".join(
        ["-" if char in AVOID_CHARACTERS else char for char in postTitle]
    )
    filteredWords = [word for word in cleanedTitle.split("-") if word]
    finalUrl = "-".join(filteredWords)
    return f"{finalUrl}".lower()


# Function to generate a unique URL ID
def generateurlID():
    newurlID = getNewUid()
    counter = 1

    while checkIfurlIDExistsInPostDb(newurlID):
        newurlID = f"{newurlID}{counter}"
        counter += 1

    return newurlID


# Test the function.
if __name__ == "__main__":
    sampleText = " 'Hello, world!' said the coder. <Can you solve this?> {It's 50% complete.} Use |pipe|, \\, ^caret^, ~tilde~, [brackets], `backtick`, 'single quote', :colon:, ;semicolon;, /slash/, ?question?, =equals=, &ampersand&, @at@, +plus+."
    print(getSlugFromPostTitle(sampleText))
