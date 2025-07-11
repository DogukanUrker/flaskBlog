"""
This module contains the code for the posts analytics page.
"""

import sqlite3

from flask import Blueprint, render_template, request, session
from settings import Settings
from utils.getAnalyticsPageData import (
    getAnalyticsPageOSGraphData,
    getAnalyticsPageTrafficGraphData,
)
from utils.log import Log

analytics_blueprint = Blueprint("analytics", __name__)


@analytics_blueprint.route("/analytics/posts/<url_id>")
def analytics_post(url_id):
    """
    This function is used to render the post analytics page.

    :param url_id: The url_id of the post.
    :type url_id: str
    :return: The rendered analytics post page.
    :rtype: flask.Response
    """
    if Settings.ANALYTICS:
        if "user_name" in session:
            connection = sqlite3.connect(Settings.DB_POSTS_ROOT)
            connection.set_trace_callback(Log.database)
            cursor = connection.cursor()

            cursor.execute("select url_id from posts")
            posts = str(cursor.fetchall())

            if url_id in posts:
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

                todays_visitor_data = getAnalyticsPageTrafficGraphData(
                    postID=post[0], hours=24
                )
                todays_visitor = 0
                for views in todays_visitor_data:
                    todays_visitor += int(views[1])

                os_graph_data = getAnalyticsPageOSGraphData(post[0])

                return render_template(
                    "postsAnalytics.html",
                    post=post,
                    todays_visitor=todays_visitor,
                    os_graph_data=os_graph_data,
                )

            else:
                Log.error(f"{request.remote_addr} tried to reach unknown post")

                return render_template("notFound.html")

        else:
            Log.error(f"{request.remote_addr} tried to reach unknown post")

            return render_template("notFound.html")

    else:
        Log.error(f"{request.remote_addr} tried to reach unknown post")

        return render_template("notFound.html")
