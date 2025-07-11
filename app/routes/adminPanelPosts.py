from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
)
from settings import Settings
from utils.log import Log
from utils.paginate import paginate_query

adminPanelPostsBlueprint = Blueprint("adminPanelPosts", __name__)


@adminPanelPostsBlueprint.route("/admin/posts", methods=["GET", "POST"])
@adminPanelPostsBlueprint.route("/adminpanel/posts", methods=["GET", "POST"])
def adminPanelPosts():
    if "userName" in session:
        Log.info(f"Admin: {session['userName']} reached to posts admin panel")
        Log.database(f"Connecting to '{Settings.DB_POSTS_ROOT}' database")

        posts, page, total_pages = paginate_query(
            Settings.DB_POSTS_ROOT,
            "select count(*) from posts",
            "select * from posts order by timeStamp desc",
        )

        Log.info(
            f"Rendering dashboard.html: params: posts={len(posts)} and showPosts=True"
        )

        return render_template(
            "dashboard.html",
            posts=posts,
            showPosts=True,
            page=page,
            total_pages=total_pages,
        )
    else:
        Log.error(
            f"{request.remote_addr} tried to reach post admin panel being logged in"
        )

        return redirect("/")
