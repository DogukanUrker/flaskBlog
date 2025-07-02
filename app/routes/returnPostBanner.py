import sqlite3
from io import BytesIO

from flask import Blueprint, request, send_file
from settings import Settings
from utils.log import Log

returnPostBannerBlueprint = Blueprint("returnPostBanner", __name__)


@returnPostBannerBlueprint.route("/postImage/<int:postID>")
def returnPostBanner(postID):
    """
    This function returns the banner image for a given post ID.

    Args:
        postID (int): The ID of the post for which the banner image is requested.

    Returns:
        The banner image for the given post ID as a Flask Response object.

    """
    Log.database(f"Connecting to '{Settings.DB_POSTS_ROOT}' database")

    connection = sqlite3.connect(Settings.DB_POSTS_ROOT)
    connection.set_trace_callback(Log.database)

    cursor = connection.cursor()

    cursor.execute(
        """select banner from posts where id = ? """,
        [(postID)],
    )

    image = BytesIO(cursor.fetchone()[0])

    Log.info(f"Post: {postID} | Image: {request.base_url} loaded")

    return send_file(image, mimetype="image/png")
