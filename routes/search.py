from helpers import (
    sqlite3,
    Blueprint,
    DB_POSTS_ROOT,
    DB_USERS_ROOT,
    render_template,
)

searchBlueprint = Blueprint("search", __name__)


@searchBlueprint.route("/search/<query>", methods=["GET", "POST"])
def search(query):
    query = query.replace("%20", " ")
    queryNoWhiteSpace = query.replace("+", "")
    query = query.replace("+", " ")
    connection = sqlite3.connect(DB_USERS_ROOT)
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
    connection = sqlite3.connect(DB_POSTS_ROOT)
    cursor = connection.cursor()
    queryTags = cursor.execute(
        """select * from posts where tags like ? """,
        [
            ("%" + query + "%"),
        ],
    ).fetchall()
    queryTitles = cursor.execute(
        """select * from posts where title like ? """,
        [
            ("%" + query + "%"),
        ],
    ).fetchall()
    queryAuthors = cursor.execute(
        """select * from posts where author like ? """,
        [
            ("%" + query + "%"),
        ],
    ).fetchall()
    queryTags = cursor.execute(
        """select * from posts where tags like ? """,
        [
            ("%" + queryNoWhiteSpace + "%"),
        ],
    ).fetchall()
    queryTitles = cursor.execute(
        """select * from posts where title like ? """,
        [
            ("%" + queryNoWhiteSpace + "%"),
        ],
    ).fetchall()
    queryAuthors = cursor.execute(
        """select * from posts where author like ? """,
        [
            ("%" + queryNoWhiteSpace + "%"),
        ],
    ).fetchall()
    posts = []
    users = []
    empty = False
    match queryTags == []:
        case False:
            posts.append(queryTags)
    match queryTitles == []:
        case False:
            posts.append(queryTitles)
    match queryAuthors == []:
        case False:
            posts.append(queryAuthors)
    match queryUsers == []:
        case False:
            users.append(queryUsers)
    match not posts and not users:
        case True:
            empty = True
    resultsID = []
    for post in posts:
        for post in post:
            match post[0] not in resultsID:
                case True:
                    resultsID.append(post[0])
    posts = []
    for postID in resultsID:
        cursor.execute(
            """select * from posts where id = ? """,
            [(postID)],
        )
        posts.append(cursor.fetchall())
    return render_template(
        "search.html",
        posts=posts,
        users=users,
        query=query,
        empty=empty,
    )
