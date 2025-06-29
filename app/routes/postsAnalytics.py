"""
This module contains the code for the posts analytics page.
"""

import sqlite3

from flask import Blueprint, render_template, request, session
from settings import ANALYTICS, DB_POSTS_ROOT
from utils.getAnalyticsPageData import (
    getAnalyticsPageOSGraphData,
    getAnalyticsPageTrafficGraphData,
)
from utils.log import Log

analyticsBlueprint = Blueprint("analytics", __name__)


@analyticsBlueprint.route("/analytics/posts/<urlID>")
def analyticsPost(urlID):
    """
    This function is used to render the post analytics page.

    :param urlID: The urlID of the post.
    :type urlID: str
    :return: The rendered analytics post page.
    :rtype: flask.Response
    """
    match ANALYTICS:
        case True:
            match "userName" in session:
                case True:
                    connection = sqlite3.connect(DB_POSTS_ROOT)
                    connection.set_trace_callback(Log.database)
                    cursor = connection.cursor()

                    cursor.execute("select urlID from posts")
                    posts = str(cursor.fetchall())

                    match urlID in posts:
                        case True:
                            Log.success(f'post: "{urlID}" loaded')

                            Log.database(f"Connecting to '{DB_POSTS_ROOT}' database")

                            connection = sqlite3.connect(DB_POSTS_ROOT)
                            connection.set_trace_callback(Log.database)
                            cursor = connection.cursor()

                            cursor.execute(
                                """select * from posts where urlID = ? """,
                                [(urlID)],
                            )
                            post = cursor.fetchone()

                            todaysVisitorData = getAnalyticsPageTrafficGraphData(
                                postID=post[0], hours=24
                            )
                            todaysVisitor = 0
                            for views in todaysVisitorData:
                                todaysVisitor += int(views[1])

                            osGraphData = getAnalyticsPageOSGraphData(post[0])

                            return render_template(
                                "postsAnalytics.html.jinja",
                                post=post,
                                todaysVisitor=todaysVisitor,
                                osGraphData=osGraphData,
                            )

                        case False:
                            Log.error(
                                f"{request.remote_addr} tried to reach unknown post"
                            )

                            return render_template("notFound.html.jinja")

                case False:
                    Log.error(f"{request.remote_addr} tried to reach unknown post")

                    return render_template("notFound.html.jinja")

        case False:
            Log.error(f"{request.remote_addr} tried to reach unknown post")

            return render_template("notFound.html.jinja")
