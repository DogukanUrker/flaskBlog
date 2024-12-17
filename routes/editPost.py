# Import necessary modules and functions
from modules import (
    Log,  # Logging module
    abort,  # Function for aborting requests
    session,  # Session management module
    sqlite3,  # SQLite database module
    request,  # Module for handling HTTP requests
    redirect,  # Function for redirecting requests
    Blueprint,  # Blueprint class for creating modular applications
    RECAPTCHA,  # Recaptcha module
    flashMessage,  # Flash messaging module
    requestsPost,  # Module for making HTTP POST requests
    DB_POSTS_ROOT,  # Path to the posts database
    DB_USERS_ROOT,  # Path to the users database
    CreatePostForm,  # Form for creating a post
    render_template,  # Function for rendering templates
    currentTimeStamp,  # Function for getting current timestamp
    RECAPTCHA_SITE_KEY,  # Recaptcha site key
    RECAPTCHA_POST_EDIT,  # # Flag for enabling/disabling Recaptcha for post editing
    RECAPTCHA_VERIFY_URL,  # Recaptcha verification URL
    RECAPTCHA_SECRET_KEY,  # Recaptcha secret key
    generateurlID,  # urlID generator from post title
)

# Create a blueprint for the edit post route
editPostBlueprint = Blueprint("editPost", __name__)


# Define a route for editing a post
@editPostBlueprint.route("/editpost/<urlID>", methods=["GET", "POST"])
def editPost(urlID):
    """
    This function handles the edit post route.

    Args:
        postID (string): the ID of the post to edit

    Returns:
        The rendered edit post template or a redirect to the homepage if the user is not authorized to edit the post

    Raises:
        abort(404): if the post does not exist
        abort(401): if the user is not authorized to edit the post
    """
    sessionUrlId = None  # if user rename post title

    # Check if "userName" exists in session
    match "userName" in session:
        case True:
            Log.sql(
                f"Connecting to '{DB_POSTS_ROOT}' database"
            )  # Log the database connection is started
            # Connect to the posts database
            connection = sqlite3.connect(DB_POSTS_ROOT)
            connection.set_trace_callback(
                Log.sql
            )  # Set the trace callback for the connection
            cursor = connection.cursor()
            cursor.execute("select urlID from posts where urlID = ?", (urlID,))
            posts = str(cursor.fetchall())
            # Check if postID exists in posts
            match str(urlID) in posts:
                case True:
                    Log.sql(
                        f"Connecting to '{DB_POSTS_ROOT}' database"
                    )  # Log the database connection is started
                    # Connect to the posts database
                    connection = sqlite3.connect(DB_POSTS_ROOT)
                    connection.set_trace_callback(
                        Log.sql
                    )  # Set the trace callback for the connection
                    cursor = connection.cursor()
                    cursor.execute(
                        """select * from posts where urlID = ? """,
                        [(urlID)],
                    )
                    post = cursor.fetchone()

                    Log.success(f'POST: "{urlID}" FOUND')
                    Log.sql(
                        f"Connecting to '{DB_USERS_ROOT}' database"
                    )  # Log the database connection is started
                    # Connect to the users database
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    connection.set_trace_callback(
                        Log.sql
                    )  # Set the trace callback for the connection
                    cursor = connection.cursor()
                    cursor.execute(
                        """select userName from users where userName = ? """,
                        [(session["userName"])],
                    )
                    # Check if the user is authorized to edit the post
                    match post[5] == session["userName"] or session[
                        "userRole"
                    ] == "admin":
                        case True:
                            # Populate the form with post data
                            form = CreatePostForm(request.form)
                            form.postTitle.data = post[1]
                            form.postTags.data = post[2]
                            form.postContent.data = post[3]
                            form.postCategory.data = post[9]
                            # Check if the request method is POST
                            match request.method == "POST":
                                case True:
                                    # Retrieve post data from the form
                                    postTitle = request.form["postTitle"]
                                    postTags = request.form["postTags"]
                                    postContent = request.form["postContent"]
                                    postCategory = request.form["postCategory"]
                                    postBanner = request.files["postBanner"].read()
                                    # Check if post content is empty
                                    match postContent == "":
                                        case True:
                                            flashMessage(
                                                page="editPost",
                                                message="empty",
                                                category="error",
                                                language=session["language"],
                                            )  # Display a flash message
                                            Log.danger(
                                                f'User: "{session["userName"]}" tried to edit a post with empty content',
                                            )
                                        case False:
                                            # check if user edited post title
                                            match postTitle == post[1]:
                                                case True:
                                                    sessionUrlId = urlID # assign existing url id   
                                                case False:
                                                    sessionUrlId = generateurlID(postTitle) # assign new url id if modified 

                                            # Check Recaptcha if enabled
                                            match RECAPTCHA and RECAPTCHA_POST_EDIT:
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
                                                    ] == True or verifyResponse[
                                                        "score"
                                                    ] > 0.5:
                                                        case True:
                                                            # Log the reCAPTCHA verification result
                                                            Log.success(
                                                                f"Post edit reCAPTCHA| verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                            )
                                                            # Update post data in the database
                                                            connection = (
                                                                sqlite3.connect(
                                                                    DB_POSTS_ROOT
                                                                )
                                                            )
                                                            connection.set_trace_callback(
                                                                Log.sql
                                                            )  # Set the trace callback for the connection
                                                            cursor = connection.cursor()
                                                            cursor.execute(
                                                                """update posts set title = ? where id = ? """,
                                                                (postTitle, post[0]),
                                                            )
                                                            cursor.execute(
                                                                """update posts set tags = ? where id = ? """,
                                                                (postTags, post[0]),
                                                            )
                                                            cursor.execute(
                                                                """update posts set content = ? where id = ? """,
                                                                (postContent, post[0]),
                                                            )
                                                            cursor.execute(
                                                                """update posts set category = ? where id = ? """,
                                                                (postCategory, post[0]),
                                                            )
                                                            match postBanner == b"":  # Check if post banner is empty
                                                                case (
                                                                    True
                                                                ):  # Do nothing if post banner is empty
                                                                    pass
                                                                case (
                                                                    False
                                                                ):  # Update post banner if not empty
                                                                    cursor.execute(
                                                                        """update posts set banner = ? where id = ? """,
                                                                        (
                                                                            postBanner,
                                                                            post[0],
                                                                        ),
                                                                    )
                                                            cursor.execute(
                                                                """update posts set lastEditTimeStamp = ? where id = ? """,
                                                                [
                                                                    (
                                                                        currentTimeStamp()
                                                                    ),
                                                                    (post[0]),
                                                                ],
                                                            )
                                                            cursor.execute(
                                                                """update posts set urlID = ? where id = ?""",
                                                                [(sessionUrlId), (post[0])],
                                                            )
                                                            connection.commit()
                                                            Log.success(
                                                                f'Post: "{postTitle}" edited',
                                                            )
                                                            flashMessage(
                                                                page="editPost",
                                                                message="success",
                                                                category="success",
                                                                language=session[
                                                                    "language"
                                                                ],
                                                            )  # Display a flash message
                                                            return redirect(
                                                                f"/post/{sessionUrlId}"
                                                            )
                                                        case False:
                                                            # Recaptcha verification failed
                                                            Log.danger(
                                                                f"Post edit reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                            )
                                                            abort(401)
                                                case False:
                                                    # Recaptcha not enabled
                                                    connection = sqlite3.connect(
                                                        DB_POSTS_ROOT
                                                    )
                                                    connection.set_trace_callback(
                                                        Log.sql
                                                    )  # Set the trace callback for the connection
                                                    cursor = connection.cursor()
                                                    cursor.execute(
                                                        """update posts set title = ? where id = ? """,
                                                        (postTitle, post[0]),
                                                    )
                                                    cursor.execute(
                                                        """update posts set tags = ? where id = ? """,
                                                        (postTags, post[0]),
                                                    )
                                                    cursor.execute(
                                                        """update posts set content = ? where id = ? """,
                                                        (postContent, post[0]),
                                                    )
                                                    cursor.execute(
                                                        """update posts set category = ? where id = ? """,
                                                        (postCategory, post[0]),
                                                    )
                                                    print(postBanner)
                                                    match postBanner == b"":  # Check if post banner is empty
                                                        case (
                                                            True
                                                        ):  # Do nothing if post banner is empty
                                                            pass
                                                        case (
                                                            False
                                                        ):  # Update post banner if not empty
                                                            cursor.execute(
                                                                """update posts set banner = ? where id = ? """,
                                                                (postBanner, post[0]),
                                                            )
                                                    cursor.execute(
                                                        """update posts set lastEditTimeStamp = ? where id = ? """,
                                                        [
                                                            (currentTimeStamp()),
                                                            (post[0]),
                                                        ],
                                                    )
                                                    cursor.execute(
                                                        """update posts set urlID = ? where id = ?""",
                                                        [(sessionUrlId), (post[0])],
                                                    )
                                                    connection.commit()
                                                    Log.success(
                                                        f'Post: "{postTitle}" edited',
                                                    )
                                                    flashMessage(
                                                        page="editPost",
                                                        message="success",
                                                        category="success",
                                                        language=session["language"],
                                                    )  # Display a flash message
                                                    return redirect(f"/post/{sessionUrlId}")
                            # Render the edit post template
                            return render_template(
                                "/editPost.html.jinja",
                                id=post[0],
                                title=post[1],
                                tags=post[2],
                                content=post[3],
                                form=form,
                                siteKey=RECAPTCHA_SITE_KEY,
                                recaptcha=RECAPTCHA,
                            )
                        case False:
                            # User is not authorized to edit the post
                            flashMessage(
                                page="editPost",
                                message="author",
                                category="error",
                                language=session["language"],
                            )  # Display a flash message
                            Log.danger(
                                f'User: "{session["userName"]}" tried to edit another authors post',
                            )
                            return redirect("/")
                case False:
                    # Post with postID does not exist
                    Log.danger(f'Post: "{urlID}" not found')
                    return render_template("notFound.html.jinja")
        case False:
            # User is not logged in
            Log.danger(f"{request.remote_addr} tried to edit post without login")
            flashMessage(
                page="editPost",
                message="login",
                category="error",
                language=session["language"],
            )  # Display a flash message
            return redirect(f"/login/redirect=&editpost&{urlID}")
