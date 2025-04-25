from modules import (
    sqlite3,
    Log,
    DB_POSTS_ROOT,
)


def getHomeFeedData(
    by="hot", sort="desc", category: str = "all", offset: int = 0, limit: int = 3
) -> list:
    Log.database(
        f"Connecting to '{DB_POSTS_ROOT}' database"
    )  # Log the database connection is started
    # Connect to the posts database
    connection = sqlite3.connect(DB_POSTS_ROOT)
    connection.set_trace_callback(
        Log.database
    )  # Set the trace callback for the connection
    # Create a cursor object for executing queries
    cursor = connection.cursor()
    # Select all the columns from the posts table and order them by the specified field and sorting order
    match category:
        case "all":
            match by:
                case "hot":  # If the sorting field is "hot"
                    cursor.execute(
                        f"SELECT id, title, content, author, timeStamp, category, urlID, (views * 1 / log(1 + (strftime('%s', 'now') - timeStamp) / 3600 + 2)) AS hotScore FROM posts ORDER BY hotScore {sort} LIMIT {limit} OFFSET {offset}"
                    )  # Execute the query to sort by hotness
                    pass
                case _:  # For all other sorting fields
                    cursor.execute(
                        f"select id, title, content, author, timeStamp, category, urlID from posts order by {by} {sort} LIMIT {limit} OFFSET {offset}"
                    )  # Execute the query to sort by the specified field
        case _:
            # Executing SQL query to retrieve posts of the requested category and sorting them accordingly
            cursor.execute(
                f"""select id, title, content, author, timeStamp, category, urlID from posts where lower(category) = ? order by {by} {sort} LIMIT {limit} OFFSET {offset}""",
                [(category.lower())],
            )
    posts = cursor.fetchall()
    # Close database connection
    connection.close()
    return posts
