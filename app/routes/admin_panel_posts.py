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

admin_panel_posts_blueprint = Blueprint("adminPanelPosts", __name__)


@admin_panel_posts_blueprint.route("/admin/posts", methods=["GET", "POST"])
@admin_panel_posts_blueprint.route("/adminpanel/posts", methods=["GET", "POST"])
def admin_panel_posts():
    if "user_name" in session:
        Log.info(f"Admin: {session['user_name']} reached to posts admin panel")
        Log.database(f"Connecting to '{Settings.DB_POSTS_ROOT}' database")

        posts, page, total_pages = paginate_query(
            Settings.DB_POSTS_ROOT,
            "select count(*) from posts",
            "select * from posts order by time_stamp desc",
        )

        Log.info(
            f"Rendering dashboard.html: params: posts={len(posts)} and show_posts=True"
        )

        return render_template(
            "dashboard.html",
            posts=posts,
            show_posts=True,
            page=page,
            total_pages=total_pages,
        )
    else:
        Log.error(
            f"{request.remote_addr} tried to reach post admin panel being logged in"
        )

        return redirect("/")
