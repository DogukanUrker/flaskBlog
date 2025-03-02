"""
This module contains the code for the user page.
"""

from modules import (
    Log,  # A class for logging messages
    sqlite3,  # A module for working with SQLite databases
    Blueprint,  # A class for creating Flask blueprints
    DB_POSTS_ROOT,  # A constant for the path to the posts database
    DB_USERS_ROOT,  # A constant for the path to the users database
    render_template,  # A function for rendering Jinja templates
    DB_COMMENTS_ROOT,  # A constant for the path to the comments database
    DB_ANALYTICS_ROOT,  # A constant for the path to the analytics database
)

analyticsBlueprint = Blueprint("analytics", __name__)  # Create a blueprint for the analytics page


@analyticsBlueprint.route("/analytics/posts/<urlID>")  # Define a route for the user page with a dynamic username parameter
def analytics(urlID):
    """
    This function is used to render the post analytics page.

    :param urlID: The urlID of the post.
    :type urlID: str
    :return: The rendered analytics post page.
    :rtype: flask.Response
    """

    connection = sqlite3.connect(DB_POSTS_ROOT)
    cursor = connection.cursor()
    cursor.execute("""select id from posts where urlID = ?""", (urlID,))
    postID = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    if postID:
        connection = sqlite3.connect(DB_POSTS_ROOT)
        cursor = connection.cursor()
        cursor.execute("""select title, urlID from posts where urlID = ?""", (urlID,))
        post = cursor.fetchone()
        cursor.close()
        connection.close()

        # graph data
        connection = sqlite3.connect(DB_ANALYTICS_ROOT)
        cursor = connection.cursor()
        cursor.execute("""select strftime('%H:%M', timeStamp, 'unixepoch') as visitDate, count(*) as totalVisit from postsAnalytics where post = ? GROUP BY visitDate""", (postID,))
        postGraphData = cursor.fetchall() or []
        print(postGraphData)

        # os data
        cursor.execute("""select os as osInfo, count(*) as osInfo from postsAnalytics where post = ? GROUP BY osInfo""", (postID,))
        postGraphOSData = cursor.fetchall() or []
        osGraphData = {
            "osList" : [os[0] for os in postGraphOSData],
            "countList" : [counts[1] for counts in postGraphOSData]
        }
        print(osGraphData)

        # country data
        cursor.execute("""select country as countryInfo, count(*) as countryInfo from postsAnalytics where post = ? GROUP BY countryInfo limit 25""", (postID,))
        postCountryData = cursor.fetchall() or []
        counryGraphData = {
            "countryList" : [country[0] for country in postCountryData],
            "countList" : [counts[1] for counts in postCountryData]
        }
        print(counryGraphData)
        cursor.close()
        connection.close()

        return render_template("analytics.html.jinja", postGraphData = postGraphData, post=post, osGraphData=osGraphData, counryGraphData=counryGraphData)