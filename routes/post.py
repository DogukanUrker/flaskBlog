# Import the necessary modules and functions
from helpers import (
    flash,
    session,
    sqlite3,
    request,
    message,
    url_for,
    APP_NAME,
    redirect,
    addPoints,
    Blueprint,
    currentDate,
    currentTime,
    commentForm,
    DB_POSTS_ROOT,
    DB_COMMENTS_ROOT,
    render_template,
)
from delete import deleteComment, deletePost

# Create a blueprint for the post route
postBlueprint = Blueprint("post", __name__)


@postBlueprint.route("/post/<int:postID>", methods=["GET", "POST"])
def post(postID):
    # Create a comment form object from the request form
    form = commentForm(request.form)
    # Connect to the posts database
    connection = sqlite3.connect(DB_POSTS_ROOT)
    cursor = connection.cursor()
    # Query the posts database for the post ID
    cursor.execute("select id from posts")
    posts = str(cursor.fetchall())
    # Check if the post ID exists in the posts database
    match str(postID) in posts:
        case True:
            # Log a message that the post is found
            message("2", f'POST: "{postID}" FOUND')
            # Connect to the posts database
            connection = sqlite3.connect(DB_POSTS_ROOT)
            cursor = connection.cursor()
            # Query the posts database for the post with the matching ID
            cursor.execute(
                """select * from posts where id = ? """,
                [(postID)],
            )
            post = cursor.fetchone()
            # Update the posts database by incrementing the views of the post by 1
            cursor.execute(
                """update posts set views = views+1 where id = ? """,
                [(postID)],
            )
            connection.commit()
            # Check if the request method is POST
            match request.method == "POST":
                case True:
                    # Check if the post delete button is clicked
                    match "postDeleteButton" in request.form:
                        case True:
                            # Delete the post from the database
                            deletePost(postID)
                            # Redirect to the home page
                            return redirect(f"/")
                    # Check if the comment delete button is clicked
                    match "commentDeleteButton" in request.form:
                        case True:
                            # Delete the comment from the database
                            deleteComment(request.form["commentID"])
                            # Redirect to the same route with a 301 status code
                            return redirect(url_for("post.post", postID=postID)), 301
                    # Get the comment from the form
                    comment = request.form["comment"]
                    # Connect to the comments database
                    connection = sqlite3.connect(DB_COMMENTS_ROOT)
                    cursor = connection.cursor()
                    # Insert the comment into the comments database with the post ID, comment, user name, date and time
                    cursor.execute(
                        "insert into comments(post,comment,user,date,time) \
                        values(?, ?, ?, ?, ?)",
                        (
                            postID,
                            comment,
                            session["userName"],
                            currentDate(),
                            currentTime(),
                        ),
                    )
                    connection.commit()
                    # Log a message that the user commented on the post
                    message(
                        "2",
                        f'USER: "{session["userName"]}" COMMENTED TO POST: "{postID}"',
                    )
                    # Add 5 points to the user's score
                    addPoints(5, session["userName"])
                    # Flash a success message to the user
                    flash("You earned 5 points by commenting ", "success")
                    # Redirect to the same route with a 301 status code
                    return redirect(url_for("post.post", postID=postID)), 301
            # Connect to the comments database
            connection = sqlite3.connect(DB_COMMENTS_ROOT)
            cursor = connection.cursor()
            # Query the comments database for the comments related to the post ID
            cursor.execute(
                """select * from comments where post = ? """,
                [(postID)],
            )
            comments = cursor.fetchall()
            # Render the post template with the post and comments data, the form object and the app name
            return render_template(
                "post.html",
                id=post[0],
                title=post[1],
                tags=post[2],
                content=post[3],
                author=post[4],
                views=post[7],
                date=post[5],
                time=post[6],
                form=form,
                comments=comments,
                appName=APP_NAME,
            )
        case False:
            # Render the 404 template if the post ID does not exist
            return render_template("404.html")
