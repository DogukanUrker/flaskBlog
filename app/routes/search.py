import sqlite3
from math import ceil

from flask import Blueprint, render_template, request
from settings import Settings
from utils.log import Log

searchBlueprint = Blueprint("search", __name__)


@searchBlueprint.route("/search/<query>", methods=["GET", "POST"])
def search(query):
    query = query.replace("%20", " ")
    queryNoWhiteSpace = query.replace("+", "")
    query = query.replace("+", " ")

    page = request.args.get("page", 1, type=int)
    per_page = 9

    Log.info(f"Searching for query: {query}")

    Log.database(f"Connecting to '{Settings.DB_USERS_ROOT}' database")

    connection = sqlite3.connect(Settings.DB_USERS_ROOT)
    connection.set_trace_callback(Log.database)
    cursor = connection.cursor()

    queryUsers = cursor.execute(
        """select * from users where userName like ? """,
        [
            ("%" + query + "%"),
        ],
    ).fetchall()

    queryUsers = cursor.execute(
        """select * from users where userName like ? """,
        [
            ("%" + queryNoWhiteSpace + "%"),
        ],
    ).fetchall()
    Log.database(f"Connecting to '{Settings.DB_POSTS_ROOT}' database")

    connection = sqlite3.connect(Settings.DB_POSTS_ROOT)
    connection.set_trace_callback(Log.database)
    cursor = connection.cursor()

    queryTags = cursor.execute(
        """select * from posts where tags like ? order by timeStamp desc""",
        [
            ("%" + query + "%"),
        ],
    ).fetchall()

    queryTitles = cursor.execute(
        """select * from posts where title like ? order by timeStamp desc""",
        [
            ("%" + query + "%"),
        ],
    ).fetchall()

    queryAuthors = cursor.execute(
        """select * from posts where author like ? order by timeStamp desc""",
        [
            ("%" + query + "%"),
        ],
    ).fetchall()

    queryTags = cursor.execute(
        """select * from posts where tags like ? order by timeStamp desc""",
        [
            ("%" + queryNoWhiteSpace + "%"),
        ],
    ).fetchall()

    queryTitles = cursor.execute(
        """select * from posts where title like ? order by timeStamp desc""",
        [
            ("%" + queryNoWhiteSpace + "%"),
        ],
    ).fetchall()

    queryAuthors = cursor.execute(
        """select * from posts where author like ? order by timeStamp desc""",
        [
            ("%" + queryNoWhiteSpace + "%"),
        ],
    ).fetchall()

    posts = []

    users = []

    empty = False

    if queryTags != []:
        posts.append(queryTags)

    if queryTitles != []:
        posts.append(queryTitles)

    if queryAuthors != []:
        posts.append(queryAuthors)

    if queryUsers != []:
        users.append(queryUsers)

    if not posts and not users:
        empty = True

    resultsID = []

    for post in posts:
        for post in post:
            if post[0] not in resultsID:
                resultsID.append(post[0])

    posts = []

    for postID in resultsID:
        cursor.execute(
            """select * from posts where id = ? """,
            [(postID)],
        )

        posts.append(cursor.fetchall())

    total_posts = len(posts)
    total_pages = max(ceil(total_posts / per_page), 1)
    offset = (page - 1) * per_page
    posts = posts[offset : offset + per_page]

    Log.info(
        f"Rendering search.html: params: query={query} | users={users} | posts={len(posts)} | empty={empty}"
    )

    return render_template(
        "search.html",
        posts=posts,
        users=users,
        query=query,
        empty=empty,
        page=page,
        total_pages=total_pages,
    )
