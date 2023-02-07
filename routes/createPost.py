from helpers import (
    session,
    sqlite3,
    request,
    flash,
    message,
    redirect,
    addPoints,
    currentDate,
    currentTime,
    render_template,
    Blueprint,
    createPostForm,
)

createPostBlueprint = Blueprint("createPost", __name__)


@createPostBlueprint.route("/createpost", methods=["GET", "POST"])
def createPost():
    match "userName" in session:
        case True:
            form = createPostForm(request.form)
            if request.method == "POST":
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
                        connection = sqlite3.connect("db/posts.db")
                        cursor = connection.cursor()
                        cursor.execute(
                            f"""
                            insert into posts(title,tags,content,author,views,date,time,lastEditDate,lastEditTime) 
                            values("{postTitle}","{postTags}","{postContent}",
                            "{session["userName"]}",0,
                            "{currentDate()}",
                            "{currentTime()}",
                            "{currentDate()}",
                            "{currentTime()}")
                            """
                        )
                        connection.commit()
                        message("2", f'POST: "{postTitle}" POSTED')
                        addPoints(20, session["userName"])
                        flash("You earned 20 points by posting ", "success")
                        return redirect("/")
            return render_template("createPost.html", form=form)
        case False:
            message("1", "USER NOT LOGGED IN")
            flash("you need loin for create a post", "error")
            return redirect("/login")
