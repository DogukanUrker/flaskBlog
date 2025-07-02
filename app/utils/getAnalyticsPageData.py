import sqlite3
from datetime import datetime, timedelta

from settings import DB_ANALYTICS_ROOT
from utils.log import Log


def getAnalyticsPageTrafficGraphData(
    postID: int, sincePosted=False, weeks: float = 0, days: float = 0, hours: float = 0
) -> list[list[int]]:
    """
    Returns the post's visitors traffic data list inside list.
    If None of below kwargs are given then default will be last 48 hours data
    Args:
        `postID` (int): The post's primary key/id whose traffic data to be retrived.
        `sincePosted` (bool): Whether to consider data since the post was created, if sincePosted is True then other kwargs will be ignored.
        `weeks` (float): Number of weeks for data retrieval.
        `days` (float): Number of days for data retrieval.
        `hours` (float): Number of hours for data retrieval.


    Returns:
        `list[list[int]]`: if none of params passed except postID function will return last 48 hours data, line graph data post traffic.
    """

    if sincePosted is not True:
        if weeks == 0 and days == 0 and hours == 0:
            hours = 48

    if sincePosted:
        sqlQuery = """select strftime('%Y-%m-%d %H:%M', timeStamp, 'unixepoch') as visitTimeStamp, count(*) as visitCount from postsAnalytics where postID = ? GROUP BY visitTimeStamp ORDER BY visitTimeStamp ASC"""
        parameter = (postID,)
    else:
        timeDeltaArgs = {"weeks": weeks or 0, "days": days or 0, "hours": hours}

        userQueryLimit = int((datetime.now() - timedelta(**timeDeltaArgs)).timestamp())

        sqlQuery = """select strftime('%Y-%m-%d %H:%M', timeStamp, 'unixepoch') as visitTimeStamp, count(*) as visitCount from postsAnalytics where postID = ? and timeStamp > ? GROUP BY visitTimeStamp ORDER BY visitTimeStamp ASC"""
        parameter = (postID, userQueryLimit)

    try:
        Log.database(f"Connecting to '{DB_ANALYTICS_ROOT}' database")

        connection = sqlite3.connect(DB_ANALYTICS_ROOT)
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()

        cursor.execute(sqlQuery, parameter)
        postTrafficData = cursor.fetchall()

        jSTimeStampAndCount = [
            [
                int((datetime.strptime(entry[0], "%Y-%m-%d %H:%M")).timestamp() * 1000),
                entry[1],
            ]
            for entry in postTrafficData
        ]

        connection.close()

        return jSTimeStampAndCount
    except Exception:
        Log.error(f"Failed to retrieve traffic data for post analytics: {postID}")
        return []


def getAnalyticsPageOSGraphData(postID: int) -> dict:
    """
    Returns the post's visitors os data list of tuples.
    Args:
        `postID` (int): The post's primary key/id whose visitors operating system counts data to be retrived.

    Returns:
        `dict`: osNameList: e.g. ["Windows", "Mac", "Android"...]. , osCountList: e.g. [3445, 6756, 53453, ...]
    """

    try:
        Log.database(f"Connecting to '{DB_ANALYTICS_ROOT}' database")

        connection = sqlite3.connect(DB_ANALYTICS_ROOT)
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()

        cursor.execute(
            """select os as osName, count(*) as osCount from postsAnalytics where postID = ? GROUP BY os""",
            (postID,),
        )
        postGraphOSData = cursor.fetchall() or []

        osGraphData = {
            "osNameList": [os[0] for os in postGraphOSData],
            "osCountList": [counts[1] for counts in postGraphOSData],
        }
        connection.close()

        return osGraphData
    except Exception:
        Log.error(f"Failed to retrieve os data for post analytics: {postID}")
        return {"osNameList": [], "osCountList": []}


def getAnalyticsPageCountryGraphData(postID: int, viewAll=False) -> dict:
    """
    Returns the post's visitors traffic data list of tuples.
    Args:
        `postID` (int): The post's primary key/id whose visitors country data to be retrieved.
        `viewAll` (bool):
            - True: Returns all data since the post was created.
            - False: Returns only the latest 25 data entries.

    Returns:
        `dict`: osNameList: e.g. ["Russia", "Germany"...]. , osCountList: e.g. [3445, 6756, ...]
    """

    if viewAll:
        sqlQuery = """select country as countryName, count(*) as countryCount from postsAnalytics where postID = ? GROUP BY country ORDER BY countryCount DESC"""
    else:
        sqlQuery = """select country as countryName, count(*) as countryCount from postsAnalytics where postID = ? GROUP BY country ORDER BY countryCount DESC limit 25"""

    try:
        Log.database(f"Connecting to '{DB_ANALYTICS_ROOT}' database")

        connection = sqlite3.connect(DB_ANALYTICS_ROOT)
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()

        cursor.execute(sqlQuery, (postID,))
        postCountryData = cursor.fetchall()

        countryGraphData = {
            "countryNameList": [country[0] for country in postCountryData],
            "countryCountList": [counts[1] for counts in postCountryData],
        }

        connection.close()

        return countryGraphData
    except Exception:
        Log.error(f"Failed to retrieve country data for post analytics: {postID}")
        return {
            "countryNameList": [],
            "countryCountList": [],
        }
