from helpers import (
    flash,
    abort,
    session,
    sqlite3,
    request,
    message,
    redirect,
    addPoints,
    Blueprint,
    RECAPTCHA,
    currentDate,
    currentTime,
    requestsPost,
    DB_POSTS_ROOT,
    createPostForm,
    render_template,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_POST_CREATE,
)

createPostBlueprint = Blueprint("createPost", __name__)


@createPostBlueprint.route("/createpost", methods=["GET", "POST"])
def createPost():
    match "userName" in session:
        case True:
            form = createPostForm(request.form)
            match request.method == "POST":
                case True:
                    postTitle = request.form["postTitle"]
                    postTags = request.form["postTags"]
                    postContent = request.form["postContent"]
                    match postContent == "":
                        case True:
                            flash("post content not be empty", "error")
                            message(
                                "1",
                                f'POST CONTENT NOT BE EMPTY USER: "{session["userName"]}"',
                            )
                        case False:
                                match RECAPTCHA and RECAPTCHA_POST_CREATE:
                                    case True:
                                        secretResponse = request.form[
                                                            "g-recaptcha-response"
                                                        ]
                                        verifyResponse = requestsPost(
                                                            url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                                        ).json()
                                        match verifyResponse[
                                                            "success"
                                                        ] == True or verifyResponse[
                                                            "score"
                                                        ] > 0.5:
                                            case True:
                                                message("2",f"POST CREATE RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                                connection = sqlite3.connect(DB_POSTS_ROOT)
                                                cursor = connection.cursor()
                                                cursor.execute(
                                                    "insert into posts(title,tags,content,author,views,date,time,lastEditDate,lastEditTime) \
                                                    values(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                                    (
                                                        postTitle,
                                                        postTags,
                                                        postContent,
                                                        session["userName"],
                                                        0,
                                                        currentDate(),
                                                        currentTime(),
                                                        currentDate(),
                                                        currentTime(),
                                                    ),
                                                )
                                                connection.commit()
                                                message("2", f'POST: "{postTitle}" POSTED')
                                                addPoints(20, session["userName"])
                                                flash("You earned 20 points by posting ", "success")
                                                return redirect("/")
                                            case False:
                                                  message("1",f"POST CREATE RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                                  abort(401)
                                    case False:
                                            connection = sqlite3.connect(DB_POSTS_ROOT)
                                            cursor = connection.cursor()
                                            cursor.execute(
                                                "insert into posts(title,tags,content,author,views,date,time,lastEditDate,lastEditTime) \
                                                values(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                                (
                                                    postTitle,
                                                    postTags,
                                                    postContent,
                                                    session["userName"],
                                                    0,
                                                    currentDate(),
                                                    currentTime(),
                                                    currentDate(),
                                                    currentTime(),
                                                ),
                                            )
                                            connection.commit()
                                            message("2", f'POST: "{postTitle}" POSTED')
                                            addPoints(20, session["userName"])
                                            flash("You earned 20 points by posting ", "success")
                                            return redirect("/") 
            return render_template("createPost.html", form=form, siteKey=RECAPTCHA_SITE_KEY, recaptcha=RECAPTCHA,)
        case False:
            message("1", "USER NOT LOGGED IN")
            flash("you need loin for create a post", "error")
            return redirect("/login/redirect=&createpost")
