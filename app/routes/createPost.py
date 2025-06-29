# Import necessary modules and functions
import sqlite3
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
)
from requests import post as requestsPost
from constants import (
    DB_POSTS_ROOT,
    RECAPTCHA,
    RECAPTCHA_POST_CREATE,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
)
from utils.log import Log
from utils.forms.CreatePostForm import CreatePostForm
from utils.flashMessage import flashMessage
from utils.addPoints import addPoints
from utils.time import currentTimeStamp
from utils.calculateReadTime import calculateReadTime
from utils.generateUrlIdFromPost import generateurlID

# Create a blueprint for the create post route
createPostBlueprint = Blueprint("createPost", __name__)


# Define a route for creating a post
@createPostBlueprint.route("/createpost", methods=["GET", "POST"])
def createPost():
    """
    This function creates a new post for the user.

    Args:
        request (Request): The request object from the user.

    Returns:
        Response: The response object with the HTML template for the create post page.

    Raises:
        401: If the user is not authenticated.
    """
    # Check if "userName" exists in session
    match "userName" in session:
        case True:
            # Create form instance
            form = CreatePostForm(request.form)
            # Check if the request method is POST
            match request.method == "POST":
                case True:
                    # Retrieve post data from the form
                    postTitle = request.form["postTitle"]
                    postTags = request.form["postTags"]
                    postContent = request.form["postContent"]
                    postBanner = request.files["postBanner"].read()
                    postCategory = request.form["postCategory"]
                    # Check if post content is empty
                    match postContent == "":
                        case True:
                            flashMessage(
                                page="createPost",
                                message="empty",
                                category="error",
                                language=session["language"],
                            )  # Display a flash message
                            Log.error(
                                f'User: "{session["userName"]}" tried to create a post with empty content',
                            )
                        case False:
                            # Check Recaptcha if enabled
                            match RECAPTCHA and RECAPTCHA_POST_CREATE:
                                case True:
                                    # Verify Recaptcha response
                                    secretResponse = request.form[
                                        "g-recaptcha-response"
                                    ]
                                    verifyResponse = requestsPost(
                                        url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                    ).json()
                                    # Check Recaptcha verification result
                                    match (
                                        verifyResponse["success"] is True
                                        or verifyResponse["score"] > 0.5
                                    ):
                                        case True:
                                            # Log the reCAPTCHA verification result
                                            Log.success(
                                                f"Post create reCAPTCHA| verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                            )
                                            Log.database(
                                                f"Connecting to '{DB_POSTS_ROOT}' database"
                                            )  # Log the database connection is started
                                            # Insert new post into the database
                                            connection = sqlite3.connect(DB_POSTS_ROOT)
                                            connection.set_trace_callback(
                                                Log.database
                                            )  # Set the trace callback for the connection
                                            cursor = connection.cursor()
                                            cursor.execute(
                                                "insert into posts(title,tags,content,banner,author,views,timeStamp,lastEditTimeStamp,category,urlID) \
                                                    values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                                (
                                                    postTitle,
                                                    postTags,
                                                    postContent,
                                                    postBanner,
                                                    session["userName"],
                                                    0,
                                                    currentTimeStamp(),
                                                    currentTimeStamp(),
                                                    postCategory,
                                                    generateurlID(postTitle),
                                                ),
                                            )
                                            connection.commit()
                                            Log.success(
                                                f'Post: "{postTitle}" posted by "{session["userName"]}"',
                                            )
                                            # Award points to the user for posting
                                            addPoints(20, session["userName"])
                                            flashMessage(
                                                page="createPost",
                                                message="success",
                                                category="success",
                                                language=session["language"],
                                            )  # Display a flash message
                                            return redirect("/")
                                        case False:
                                            # Recaptcha verification failed
                                            Log.error(
                                                f"Post create reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                            )
                                            abort(401)
                                case False:
                                    # Recaptcha not enabled
                                    Log.database(
                                        f"Connecting to '{DB_POSTS_ROOT}' database"
                                    )  # Log the database connection is started
                                    connection = sqlite3.connect(DB_POSTS_ROOT)
                                    connection.set_trace_callback(
                                        Log.database
                                    )  # Set the trace callback for the connection
                                    cursor = connection.cursor()
                                    cursor.execute(
                                        "insert into posts(title,tags,content,banner,author,views,timeStamp,lastEditTimeStamp,category,urlID) \
                                                    values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                        (
                                            postTitle,
                                            postTags,
                                            postContent,
                                            postBanner,
                                            session["userName"],
                                            0,
                                            currentTimeStamp(),
                                            currentTimeStamp(),
                                            postCategory,
                                            generateurlID(),
                                        ),
                                    )
                                    connection.commit()
                                    Log.success(
                                        f'Post: "{postTitle}" posted by "{session["userName"]}"',
                                    )
                                    # Award points to the user for posting
                                    addPoints(20, session["userName"])
                                    flashMessage(
                                        page="createPost",
                                        message="success",
                                        category="success",
                                        language=session["language"],
                                    )  # Display a flash message
                                    return redirect("/")
            # Render the create post template
            return render_template(
                "createPost.html.jinja",
                form=form,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
        case False:
            # User is not logged in
            Log.error(f"{request.remote_addr} tried to create a new post without login")
            flashMessage(
                page="createPost",
                message="login",
                category="error",
                language=session["language"],
            )  # Display a flash message
            return redirect("/login/redirect=&createpost")
