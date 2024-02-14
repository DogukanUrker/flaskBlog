# Import necessary modules and functions
from modules import (
    Log,  # Logging module
    flash,  # Flash messaging module
    abort,  # Function for aborting requests
    session,  # Session management module
    sqlite3,  # SQLite database module
    request,  # Module for handling HTTP requests
    redirect,  # Function for redirecting requests
    addPoints,  # Function for adding points to a user
    Blueprint,  # Blueprint class for creating modular applications
    RECAPTCHA,  # Recaptcha module
    requestsPost,  # Module for making HTTP POST requests
    DB_POSTS_ROOT,  # Path to the posts database
    CreatePostForm,  # Form for creating a post
    render_template,  # Function for rendering templates
    currentTimeStamp,  # Function for getting current timestamp
    RECAPTCHA_SITE_KEY,  # Recaptcha site key
    RECAPTCHA_VERIFY_URL,  # Recaptcha verification URL
    RECAPTCHA_SECRET_KEY,  # Recaptcha secret key
    RECAPTCHA_POST_CREATE,  # Flag for enabling/disabling Recaptcha for post creation
)

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
                            # Flash an error message
                            flash("Post content not be empty.", "error")
                            Log.danger(
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
                                    match verifyResponse[
                                        "success"
                                    ] == True or verifyResponse["score"] > 0.5:
                                        case True:
                                            # Log the reCAPTCHA verification result
                                            Log.success(
                                                f"Post create reCAPTCHA| verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                            )
                                            Log.sql(
                                                f"Connecting to '{DB_POSTS_ROOT}' database"
                                            )  # Log the database connection is started
                                            # Insert new post into the database
                                            connection = sqlite3.connect(DB_POSTS_ROOT)
                                            connection.set_trace_callback(
                                                Log.sql
                                            )  # Set the trace callback for the connection
                                            cursor = connection.cursor()
                                            cursor.execute(
                                                "insert into posts(title,tags,content,banner,author,views,timeStamp,lastEditTimeStamp,category) \
                                                    values(?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
                                                ),
                                            )
                                            connection.commit()
                                            Log.success(
                                                f'Post: "{postTitle}" posted by "{session["userName"]}"',
                                            )
                                            # Award points to the user for posting
                                            addPoints(20, session["userName"])
                                            flash(
                                                "You earned 20 points by posting.",
                                                "success",
                                            )
                                            return redirect("/")
                                        case False:
                                            # Recaptcha verification failed
                                            Log.danger(
                                                f"Post create reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                            )
                                            abort(401)
                                case False:
                                    # Recaptcha not enabled
                                    Log.sql(
                                        f"Connecting to '{DB_POSTS_ROOT}' database"
                                    )  # Log the database connection is started
                                    connection = sqlite3.connect(DB_POSTS_ROOT)
                                    connection.set_trace_callback(
                                        Log.sql
                                    )  # Set the trace callback for the connection
                                    cursor = connection.cursor()
                                    cursor.execute(
                                        "insert into posts(title,tags,content,banner,author,views,timeStamp,lastEditTimeStamp,category) \
                                                    values(?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
                                        ),
                                    )
                                    connection.commit()
                                    Log.success(
                                        f'Post: "{postTitle}" posted by "{session["userName"]}"',
                                    )
                                    # Award points to the user for posting
                                    addPoints(20, session["userName"])
                                    flash("You earned 20 points by posting.", "success")
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
            Log.danger(
                f"{request.remote_addr} tried to create a new post without login"
            )
            flash("You need loin for create a post.", "error")
            return redirect("/login/redirect=&createpost")
