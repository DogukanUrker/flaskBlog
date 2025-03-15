from modules import DB_POSTS_ROOT, Log, sqlite3, uuid


# Function to check if URL ID exists in the database
def checkIfurlIDExistsInPostDb(urlID):
    with sqlite3.connect(DB_POSTS_ROOT) as connection:
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()
        cursor.execute("SELECT urlID FROM posts WHERE urlID = ?", (urlID,))
        return bool(cursor.fetchall())


# Characters to remove for post title that causes issues
AVOID_CHARACTERS = [
    " ",  # Space
    "<",  # Less than
    ">",  # Greater than
    "#",  # Hash
    "%",  # Percent
    "{",  # Curly braces
    "}",  # Curly braces
    "|",  # Pipe
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
]  # Characters to avoid in post title for URL ID generation function to work properly. Add more characters if needed.


# Function to generate a new unique ID
def getNewUid():
    return str(uuid.uuid4())[24:]


# Function to convert post title to URL ID
def convertPostTitleTourlID(postTitle):
    cleanedTitle = "".join(
        ["-" if char in AVOID_CHARACTERS else char for char in postTitle]
    )
    filteredWords = [word for word in cleanedTitle.split("-") if word]
    finalUrl = "-".join(filteredWords)
    return f"{finalUrl}-{getNewUid()}".lower()


# Function to generate a unique URL ID
def generateurlID(postTitle):
    baseurlID = convertPostTitleTourlID(postTitle)
    newurlID = baseurlID
    counter = 1

    while checkIfurlIDExistsInPostDb(newurlID):
        newurlID = f"{baseurlID}-{counter}"
        counter += 1

    return newurlID


# Test the function.
if __name__ == "__main__":
    sampleText = " 'Hello, world!' said the coder. <Can you solve this?> {It's 50% complete.} Use |pipe|, \\, ^caret^, ~tilde~, [brackets], `backtick`, 'single quote', :colon:, ;semicolon;, /slash/, ?question?, =equals=, &ampersand&, @at@, +plus+."
    print(convertPostTitleTourlID(sampleText))
