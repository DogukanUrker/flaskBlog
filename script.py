import sqlite3

# Connect to the posts database
connection = sqlite3.connect('db/posts.db')
cursor = connection.cursor()

# Rename the column from urlId to urlID
cursor.execute('ALTER TABLE posts RENAME COLUMN urlId TO urlID;')

# Commit the changes and close the connection
connection.commit()
connection.close()