"""
This module contains the code for the user page.
"""

from modules import (
    Log,  # A class for logging messages
    sqlite3,  # A module for working with SQLite databases
    Blueprint,  # A class for creating Flask blueprints
    DB_POSTS_ROOT,  # A constant for the path to the posts database
    DB_USERS_ROOT,  # A constant for the path to the users database
    render_template,  # A function for rendering Jinja templates
    DB_COMMENTS_ROOT,  # A constant for the path to the comments database
)

userBlueprint = Blueprint("user", __name__)  # Create a blueprint for the user page


@userBlueprint.route(
    "/user/<userName>"
)  # Define a route for the user page with a dynamic username parameter
def user(userName):
    """
    This function is used to render the user page.

    :param userName: The username of the user.
    :type userName: str
    :return: The rendered user page.
    :rtype: flask.Response
    """
    userName = userName.lower()  # Convert the username to lowercase for consistency
    Log.sql(
        f"Connecting to '{DB_USERS_ROOT}' database"
    )  # Log the database connection is started
    connection = sqlite3.connect(DB_USERS_ROOT)  # Connect to the users database
    connection.set_trace_callback(Log.sql)  # Set the trace callback for the connection
    cursor = connection.cursor()  # Create a cursor object for executing queries
    cursor.execute(
        f"select userName from users"
    )  # Select all the usernames from the users table
    users = cursor.fetchall()  # Fetch all the results as a list of tuples
    """
    This match statement checks if the given username exists in the database.
    If the username exists, the function fetches the user details and the number of views their posts have received.
    It also fetches all the posts made by the user and all the comments made by the user.
    """
    match userName in str(
        users
    ).lower():  # Use a match statement to compare the username with the list of usernames
        case True:  # If the username exists
            Log.success(
                f'User: "{userName}" found'
            )  # Log a message with level 2 indicating the user was found
            cursor.execute(
                """select * from users where lower(userName) = ? """,  # Select all the columns from the users table where the username matches the given username
                [(userName)],  # Use a parameterized query to avoid SQL injection
            )
            user = cursor.fetchone()  # Fetch the first result as a tuple
            Log.sql(
                f"Connecting to '{DB_POSTS_ROOT}' database"
            )  # Log the database connection is started
            connection = sqlite3.connect(DB_POSTS_ROOT)  # Connect to the posts database
            connection.set_trace_callback(
                Log.sql
            )  # Set the trace callback for the connection
            cursor = (
                connection.cursor()
            )  # Create a new cursor object for executing queries
            cursor.execute(
                """select views from posts where author = ? order by timeStamp desc""",  # Select the views column from the posts table where the author matches the user's name and order by the timestamp in descending order
                [
                    (user[1])
                ],  # Use the second element of the user tuple as the author name
            )
            viewsData = cursor.fetchall()  # Fetch all the results as a list of tuples
            views = 0  # Initialize a variable for storing the total number of views
            for view in viewsData:  # Loop through each tuple in the list
                views += int(
                    view[0]
                )  # Add the first element of the tuple (the view count) to the total views
            cursor.execute(
                """select * from posts where author = ? order by timeStamp desc""",  # Select all the columns from the posts table where the author matches the user's name and order by the timestamp in descending order
                [
                    (user[1])
                ],  # Use the second element of the user tuple as the author name
            )
            posts = cursor.fetchall()  # Fetch all the results as a list of tuples
            connection = sqlite3.connect(
                DB_COMMENTS_ROOT
            )  # Connect to the comments database
            connection.set_trace_callback(
                Log.sql
            )  # Set the trace callback for the connection
            cursor = (
                connection.cursor()
            )  # Create a new cursor object for executing queries
            cursor.execute(
                """select * from comments where lower(user) = ? """,  # Select all the columns from the comments table where the user matches the given username
                [(userName.lower())],  # Use the lowercase version of the username
            )
            comments = cursor.fetchall()  # Fetch all the results as a list of tuples
            """
            This match statement checks if the user has any posts or comments.
            If the user has any posts, the variable showPosts is set to True.
            If the user has any comments, the variable showComments is set to True.
            """
            match posts:  # Use a match statement to compare the posts list with an empty list
                case []:  # If the posts list is empty
                    showPosts = False  # Set the showPosts variable to False
                case _:  # If the posts list is not empty
                    showPosts = True  # Set the showPosts variable to True
            match comments:  # Use a match statement to compare the comments list with an empty list
                case []:  # If the comments list is empty
                    showComments = False  # Set the showComments variable to False
                case _:  # If the comments list is not empty
                    showComments = True  # Set the showComments variable to True
            Log.success(
                f'User: "{userName}"s data loaded'
            )  # Log a message with level 2 indicating the user's page was loaded
            return render_template(  # Return the rendered template of the user page
                "user.html.jinja",  # The name of the template file
                user=user,  # Pass the user tuple as a keyword argument
                views=views,  # Pass the total views as a keyword argument
                posts=posts,  # Pass the posts list as a keyword argument
                comments=comments,  # Pass the comments list as a keyword argument
                showPosts=showPosts,  # Pass the showPosts variable as a keyword argument
                showComments=showComments,  # Pass the showComments variable as a keyword argument
            )
        case _:  # If the username does not exist
            Log.danger(
                f'User: "{userName}" not found'
            )  # Log an error message the user was not found
            return render_template(
                "notFound.html.jinja"
            )  # Return the rendered template of the not found page
