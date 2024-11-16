"""
This modules contains code of post title to url id generator 
"""

from modules import (
    DB_POSTS_ROOT, # Root directory path for the posts database
    Log,
    sqlite3 
)

# function to check url id exist or not in database
def checkIfUrlIdExistPostDb(urlId):
    with sqlite3.connect(DB_POSTS_ROOT) as connection:
        connection.set_trace_callback(Log.sql)
        cursor = connection.cursor()
        s = cursor.execute("""SELECT urlId from posts WHERE urlId = ? """, (urlId,))
        result = s.fetchall()
        if result:
            return True # urlId already exist in db
        else:
            return False # urlId does not exist in db

# characters to remove for post title that causes issue 
avoid_characters = [
    ' ',  # Space
    '<', '>',  # Angle brackets
    '#',  # Hash
    '%',  # Percent
    '{', '}',  # Curly braces
    '|',  # Pipe
    '\\',  # Backslash
    '^',  # Caret
    '~',  # Tilde
    '[', ']',  # Square brackets
    '`',  # Backtick
    '"',  # Double quote
    "'",  # Single quote
    ':',  # Colon
    ';',  # Semicolon
    '/',  # Slash
    '?',  # Question mark
    '=',  # Equals
    '&',  # Ampersand
    '@',  # At symbol
    '+',  # Plus sign
    '.',   # full stop
    ','   # comma
]

# sample text
text = " 'Hello, world!' said the coder. <Can you solve this?> {It's 50% complete.} Use |pipe|, \\, ^caret^, ~tilde~, [brackets], `backtick`, 'single quote', :colon:, ;semicolon;, /slash/, ?question?, =equals=, &ampersand&, @at@, +plus+."

def getNewUid():
    import uuid
    uniqueID = str(uuid.uuid4())[24:]
    return uniqueID

def convertPostTitleInUrlId(postTitle):
    cleanedTitle = postTitle
    filteredWords = []
    final_url = ""

    # Replace avoidable characters with a hyphen
    for char in avoid_characters:
        cleanedTitle = cleanedTitle.replace(char, "-")

    # Split the string into words using hyphen as a separator
    filteredWords = cleanedTitle.split("-")

    # Reconstruct the string, avoiding empty strings
    for word in filteredWords:
        if word:  # Skip empty words
            final_url = f"{final_url}-{word}"

    # Generate the final URL ID by appending a unique ID
    url_id = f"{final_url.strip('-')}-{getNewUid()}".lower()

    return url_id

def generateUrlId(postTitle):
    baseUrlId = convertPostTitleInUrlId(postTitle)
    newUrlId = baseUrlId
    counter = 1
    
    # Check if the ID exists and modify it if necessary
    while checkIfUrlIdExistPostDb(newUrlId):
        newUrlId = f"{baseUrlId}-{counter}"
        counter += 1

    return newUrlId


if __name__== "__main__":
    convertPostTitleInUrlId(text)