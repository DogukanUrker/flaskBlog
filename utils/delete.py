"""
This module contains the database delete functions for the app.

The functions in this module are responsible for managing the database
and interacting with the posts, users, and comments tables.

The functions in this module are:

- deletePost(postID): This function deletes a post and all associated comments
from the database.
- deleteUser(userName): This function deletes a user and all associated data
from the database.
- deleteComment(commentID): This function deletes a comment from the database.

The functions in this module use the following helper functions:

- flash(message, category): This function flashes a message to the user.
- Log.{type}(message): This function sends a message to the server.
- session: This variable stores information about the current user's session.
- redirect(url): This function redirects the user to a new URL.
- DB_POSTS_ROOT: This variable stores the path to the posts database.
- DB_USERS_ROOT: This variable stores the path to the users database.
- DB_COMMENTS_ROOT: This variable stores the path to the comments database.
"""

from modules import (
    Log,  # A class for logging messages
    flash,  # A function for displaying flash messages
    sqlite3,  # A module for working with SQLite databases
    session,  # A dictionary for storing session data
    redirect,  # A function for returning redirect responses
    DB_POSTS_ROOT,  # A constant for the path to the posts database
    DB_USERS_ROOT,  # A constant for the path to the users database
    DB_COMMENTS_ROOT,  # A constant for the path to the comments database
)


class Delete:
    def post(postID):
        """
        This function deletes a post and all associated comments from the database.

        Parameters:
        postID (str): The ID of the post to be deleted.

        Returns:
        None
        """
        Log.sql(
            f"Connecting to '{DB_POSTS_ROOT}' database"
        )  # Log the database connection is started
        connection = sqlite3.connect(DB_POSTS_ROOT)  # Connect to the posts database
        connection.set_trace_callback(
            Log.sql
        )  # Set the trace callback for the connection
        cursor = connection.cursor()  # Create a cursor object for executing queries
        cursor.execute(
            """select author from posts where id = ? """,  # Select the author column from the posts table where the id matches the given postID
            [(postID)],  # Use a parameterized query to avoid SQL injection
        )
        cursor.execute(
            """delete from posts where id = ? """,  # Delete the row from the posts table where the id matches the given postID
            [(postID)],  # Use a parameterized query to avoid SQL injection
        )
        cursor.execute(
            "update sqlite_sequence set seq = seq-1"
        )  # Update the sqlite_sequence table to decrement the sequence value by 1
        connection.commit()  # Commit the changes to the database
        connection.close()  # Close the connection to the database
        connection = sqlite3.connect(
            DB_COMMENTS_ROOT
        )  # Connect to the comments database
        connection.set_trace_callback(
            Log.sql
        )  # Set the trace callback for the connection
        cursor = connection.cursor()  # Create a new cursor object for executing queries
        cursor.execute(
            """select count(*) from comments where post = ? """,  # Select the count of rows from the comments table where the post column matches the given postID
            [(postID)],  # Use a parameterized query to avoid SQL injection
        )
        commentCount = list(cursor)[0][
            0
        ]  # Convert the result to a list and get the first element of the first tuple (the count value)
        cursor.execute(
            """delete from comments where post = ? """,  # Delete the rows from the comments table where the post column matches the given postID
            [(postID)],  # Use a parameterized query to avoid SQL injection
        )
        cursor.execute(
            """update sqlite_sequence set seq = seq - ? """,  # Update the sqlite_sequence table to decrement the sequence value by the commentCount
            [(commentCount)],  # Use a parameterized query to avoid SQL injection
        )
        connection.commit()  # Commit the changes to the database
        flash(
            f"Post: {postID} deleted.", "error"
        )  # Display a flash message with the text "post deleted" and the category "error"
        Log.success(
            f'Post: "{postID}" deleted'
        )  # Log a message with level 2 indicating the post was deleted

    def user(userName):
        """
        This function deletes a user and all associated data from the database.

        Parameters:
        userName (str): The username of the user to be deleted.

        Returns:
        None
        """
        Log.sql(
            f"Connecting to '{DB_USERS_ROOT}' database"
        )  # Log the database connection is started
        connection = sqlite3.connect(DB_USERS_ROOT)  # Connect to the users database
        connection.set_trace_callback(
            Log.sql
        )  # Set the trace callback for the connection
        cursor = connection.cursor()  # Create a cursor object for executing queries
        cursor.execute(
            """select * from users where lower(userName) = ? """,  # Select all the columns from the users table where the lowercased userName column matches the lowercased given userName
            [
                (userName.lower())
            ],  # Use the lowercased version of the userName and a parameterized query to avoid SQL injection
        )
        cursor.execute(
            """select role from users where userName = ? """,  # Select the role column from the users table where the userName column matches the userName stored in the session dictionary
            [
                (session["userName"])
            ],  # Use the userName from the session dictionary and a parameterized query to avoid SQL injection
        )
        perpetrator = cursor.fetchone()  # Fetch the first result as a tuple
        cursor.execute(
            """delete from users where lower(userName) = ? """,  # Delete the row from the users table where the lowercased userName column matches the lowercased given userName
            [
                (userName.lower())
            ],  # Use the lowercased version of the userName and a parameterized query to avoid SQL injection
        )
        cursor.execute(
            "update sqlite_sequence set seq = seq-1"
        )  # Update the sqlite_sequence table to decrement the sequence value by 1
        connection.commit()  # Commit the changes to the database
        flash(
            f"User: {userName} deleted.", "error"
        )  # Display a flash message with the text "user: {userName} deleted" and the category "error"
        Log.success(
            f'User: "{userName}" deleted'
        )  # Log a message with level 2 indicating the user was deleted
        match perpetrator[
            0
        ] == "admin":  # Use a match statement to compare the first element of the perpetrator tuple (the role) with the string "admin"
            case True:  # If the perpetrator is an admin
                return redirect(
                    f"/admin/users"
                )  # Return a redirect response to the admin users page
            case False:  # If the perpetrator is not an admin
                session.clear()  # Clear the session dictionary
                return redirect(f"/")  # Return a redirect response to the home page

    def comment(commentID):
        """
        This function deletes a comment from the database.

        Parameters:
        commentID (str): The ID of the comment to be deleted.

        Returns:
        None
        """
        connection = sqlite3.connect(
            DB_COMMENTS_ROOT
        )  # Connect to the comments database
        connection.set_trace_callback(
            Log.sql
        )  # Set the trace callback for the connection
        cursor = connection.cursor()  # Create a cursor object for executing queries
        cursor.execute(
            """select user from comments where id = ? """,  # Select the user column from the comments table where the id matches the given commentID
            [(commentID)],  # Use a parameterized query to avoid SQL injection
        )
        cursor.execute(
            """delete from comments where id = ? """,  # Delete the row from the comments table where the id matches the given commentID
            [(commentID)],  # Use a parameterized query to avoid SQL injection
        )
        cursor.execute(
            "update sqlite_sequence set seq = seq-1"
        )  # Update the sqlite_sequence table to decrement the sequence value by 1
        connection.commit()  # Commit the changes to the database
        flash(
            f"Comment: {commentID} deleted.", "error"
        )  # Display a flash message with the text "comment deleted" and the category "error"
        Log.success(
            f'Comment: "{commentID}" deleted'
        )  # Log a message with level 2 indicating the comment was deleted
