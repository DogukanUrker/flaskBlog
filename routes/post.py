# Import necessary modules and functions
from modules import (
    Log,  # Custom logging module
    Delete,  # Module for deleting posts and comments
    session,  # Session management module
    sqlite3,  # SQLite database module
    request,  # Request handling module
    url_for,  # URL generation module
    APP_NAME,  # Application name
    redirect,  # Redirect function
    addPoints,  # Function to add points to user's score
    Blueprint,  # Blueprint for defining routes
    CommentForm,  # Form class for comments
    flashMessage,  # Flash messaging module
    DB_POSTS_ROOT,  # Path to the posts database
    currentTimeStamp,  # Function to get current timestamp
    DB_COMMENTS_ROOT,  # Path to the comments database
    render_template,  # Template rendering function
)

# Create a blueprint for the post route
postBlueprint = Blueprint("post", __name__)


# Define the route handler for individual posts
@postBlueprint.route("/post/<urlID>", methods=["GET", "POST"])
def post(urlID):
    # Create a comment form object from the request form
    form = CommentForm(request.form)

    Log.sql(
        f"Connecting to '{DB_POSTS_ROOT}' database"
    )  # Log the database connection is started
    # Connect to the posts database
    connection = sqlite3.connect(DB_POSTS_ROOT)
    connection.set_trace_callback(Log.sql)  # Set the trace callback for the connection
    cursor = connection.cursor()

    # Query the posts database for all post url IDs
    cursor.execute("select urlID from posts")
    posts = str(cursor.fetchall())

    # Check if the requested post ID exists in the posts database
    match str(urlID) in posts:
        case True:
            # Log a message indicating that the post is found
            Log.success(f'post: "{urlID}" loaded')

            Log.sql(
                f"Connecting to '{DB_POSTS_ROOT}' database"
            )  # Log the database connection is started
            # Connect to the posts database
            connection = sqlite3.connect(DB_POSTS_ROOT)
            connection.set_trace_callback(
                Log.sql
            )  # Set the trace callback for the connection
            cursor = connection.cursor()

            # Query the posts database for the post with the matching url ID
            cursor.execute(
                """select * from posts where urlID = ? """,
                [(urlID)],
            )
            post = cursor.fetchone()

            # Increment the views of the post by 1 in the posts database
            cursor.execute(
                """update posts set views = views+1 where id = ? """,
                [(post[0])],
            )
            connection.commit()

            # Handle POST requests
            match request.method == "POST":
                case True:
                    # Check if the post delete button is clicked
                    match "postDeleteButton" in request.form:
                        case True:
                            # Delete the post from the database
                            Delete.post(post[0])
                            # Redirect to the home page
                            return redirect(f"/")

                    # Check if the comment delete button is clicked
                    match "commentDeleteButton" in request.form:
                        case True:
                            # Delete the comment from the database
                            Delete.comment(request.form["commentID"])
                            # Redirect to the same route with a 301 status code
                            return redirect(url_for("post.post", urlID=urlID)), 301

                    # Get the comment from the form
                    comment = request.form["comment"]

                    Log.sql(
                        f"Connecting to '{DB_COMMENTS_ROOT}' database"
                    )  # Log the database connection is started
                    # Connect to the comments database
                    connection = sqlite3.connect(DB_COMMENTS_ROOT)
                    connection.set_trace_callback(
                        Log.sql
                    )  # Set the trace callback for the connection
                    cursor = connection.cursor()

                    # Insert the comment into the comments database with the post ID, comment, user name, date, and time
                    cursor.execute(
                        "insert into comments(post,comment,user,timeStamp) \
                        values(?, ?, ?, ?)",
                        (
                            post[0],
                            comment,
                            session["userName"],
                            currentTimeStamp(),
                        ),
                    )
                    connection.commit()

                    # Log a message indicating that the user commented on the post
                    Log.success(
                        f'User: "{session["userName"]}" commented to post: "{urlID}"',
                    )

                    # Add 5 points to the user's score
                    addPoints(5, session["userName"])

                    flashMessage(
                        page="post",
                        message="success",
                        category="success",
                        language=session["language"],
                    )  # Display a flash message

                    # Redirect to the same route with a 301 status code
                    return redirect(url_for("post.post", urlID=urlID)), 301

            Log.sql(
                f"Connecting to '{DB_COMMENTS_ROOT}' database"
            )  # Log the database connection is started
            # Connect to the comments database
            connection = sqlite3.connect(DB_COMMENTS_ROOT)
            connection.set_trace_callback(
                Log.sql
            )  # Set the trace callback for the connection
            cursor = connection.cursor()

            # Query the comments database for the comments related to the post ID
            cursor.execute(
                """select * from comments where post = ? order by timeStamp desc""",
                [(post[0])],
            )
            comments = cursor.fetchall()

            # Render the post template with the post and comments data, the form object, and the app name
            return render_template(
                "post.html.jinja",
                id=post[0],
                title=post[1],
                tags=post[2],
                content=post[3],
                author=post[5],
                views=post[6],
                timeStamp=post[7],
                lastEditTimeStamp=post[8],
                urlID=post[10],
                form=form,
                comments=comments,
                appName=APP_NAME,
                blogPostUrl=request.root_url,
            )

        case False:
            Log.danger(
                f"{request.remote_addr} tried to reach unknown post"
            )  # Log a message with level 1 indicating the post is not found
            # Render the 404 template if the post ID does not exist
            return render_template("notFound.html.jinja")
