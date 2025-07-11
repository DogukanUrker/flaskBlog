import sqlite3

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from settings import Settings
from utils.addPoints import add_points
from utils.calculateReadTime import calculate_read_time
from utils.delete import Delete
from utils.flashMessage import flash_message
from utils.forms.CommentForm import CommentForm
from utils.generateUrlIdFromPost import get_slug_from_post_title
from utils.getDataFromUserIP import getDataFromUserIP
from utils.log import Log
from utils.time import current_time_stamp

post_blueprint = Blueprint("post", __name__)


@post_blueprint.route("/post/<url_id>", methods=["GET", "POST"])
@post_blueprint.route("/post/<slug>-<url_id>", methods=["GET", "POST"])
def post(url_id=None, slug=None):
    form = CommentForm(request.form)

    Log.database(f"Connecting to '{Settings.DB_POSTS_ROOT}' database")

    connection = sqlite3.connect(Settings.DB_POSTS_ROOT)
    connection.set_trace_callback(Log.database)
    cursor = connection.cursor()

    cursor.execute("select url_id, title from posts where url_id = ?", (url_id,))
    posts = cursor.fetchone()

    if str(url_id) in posts:
        post_slug = get_slug_from_post_title(posts[1])

        if slug != post_slug:
            return redirect(url_for("post.post", url_id=url_id, slug=post_slug))

        Log.success(f'post: "{url_id}" loaded')

        Log.database(f"Connecting to '{Settings.DB_POSTS_ROOT}' database")

        connection = sqlite3.connect(Settings.DB_POSTS_ROOT)
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()

        cursor.execute(
            """select * from posts where url_id = ? """,
            [(url_id)],
        )
        post = cursor.fetchone()

        cursor.execute(
            """update posts set views = views+1 where id = ? """,
            [(post[0])],
        )
        connection.commit()

        if request.method == "POST":
            if "postDeleteButton" in request.form:
                Delete.post(post[0])

                return redirect("/")

            if "commentDeleteButton" in request.form:
                Delete.comment(request.form["commentID"])

                return redirect(url_for("post.post", url_id=url_id)), 301

            from markupsafe import escape

            comment = escape(request.form["comment"])

            Log.database(f"Connecting to '{Settings.DB_COMMENTS_ROOT}' database")

            connection = sqlite3.connect(Settings.DB_COMMENTS_ROOT)
            connection.set_trace_callback(Log.database)
            cursor = connection.cursor()

            cursor.execute(
                "insert into comments(post,comment,user,time_stamp) \
                values(?, ?, ?, ?)",
                (
                    post[0],
                    comment,
                    session["user_name"],
                    current_time_stamp(),
                ),
            )
            connection.commit()

            Log.success(
                f'User: "{session["user_name"]}" commented to post: "{url_id}"',
            )

            add_points(5, session["user_name"])

            flash_message(
                page="post",
                message="success",
                category="success",
                language=session["language"],
            )

            return redirect(url_for("post.post", url_id=url_id)), 301

        Log.database(f"Connecting to '{Settings.DB_COMMENTS_ROOT}' database")

        connection = sqlite3.connect(Settings.DB_COMMENTS_ROOT)
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()

        cursor.execute(
            """select * from comments where post = ? order by time_stamp desc""",
            [(post[0])],
        )
        comments = cursor.fetchall()

        if Settings.ANALYTICS:
            user_ip_data = getDataFromUserIP(str(request.headers.get("User-Agent")))
            id_for_random_visitor = None
            if "user_name" in session:
                session_user = session["user_name"]
            else:
                session_user = "unsignedUser"
            if user_ip_data["status"] == 0:
                Log.database(f"Connecting to '{Settings.DB_ANALYTICS_ROOT}' database")

                connection = sqlite3.connect(Settings.DB_ANALYTICS_ROOT)
                connection.set_trace_callback(Log.database)
                cursor = connection.cursor()

                cursor.execute(
                    """insert into postsAnalytics (postID, visitorUserName, country, os, continent, time_stamp) values (?,?,?,?,?,?) RETURNING id""",
                    (
                        post[0],
                        session_user,
                        user_ip_data["payload"]["country"],
                        user_ip_data["payload"]["os"],
                        user_ip_data["payload"]["continent"],
                        current_time_stamp(),
                    ),
                )
                id_for_random_visitor = cursor.fetchone()[0]
                connection.commit()
                connection.close()
            else:
                Log.error(f"Aborting postsAnalytics, {user_ip_data['message']}")
        else:
            id_for_random_visitor = None

        return render_template(
            "post.html",
            id=post[0],
            title=post[1],
            tags=post[2],
            abstract=post[11],
            content=post[3],
            author=post[5],
            views=post[6],
            time_stamp=post[7],
            last_edit_time_stamp=post[8],
            url_id=post[10],
            form=form,
            comments=comments,
            appName=Settings.APP_NAME,
            blogPostUrl=request.root_url,
            readingTime=calculate_read_time(post[3]),
            id_for_random_visitor=id_for_random_visitor,
        )

    else:
        Log.error(f"{request.remote_addr} tried to reach unknown post")

        return render_template("notFound.html")
