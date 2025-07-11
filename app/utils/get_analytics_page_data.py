import sqlite3
from datetime import datetime, timedelta

from settings import Settings
from utils.log import Log


def get_analytics_page_traffic_graph_data(
    post_id: int,
    since_posted=False,
    weeks: float = 0,
    days: float = 0,
    hours: float = 0,
) -> list[list[int]]:
    """
    Returns the post's visitors traffic data list inside list.
    If None of below kwargs are given then default will be last 48 hours data
    Args:
        `post_id` (int): The post's primary key/id whose traffic data to be retrived.
        `since_posted` (bool): Whether to consider data since the post was created, if since_posted is True then other kwargs will be ignored.
        `weeks` (float): Number of weeks for data retrieval.
        `days` (float): Number of days for data retrieval.
        `hours` (float): Number of hours for data retrieval.


    Returns:
        `list[list[int]]`: if none of params passed except post_id function will return last 48 hours data, line graph data post traffic.
    """

    if since_posted is not True:
        if weeks == 0 and days == 0 and hours == 0:
            hours = 48

    if since_posted:
        sql_query = """select strftime('%Y-%m-%d %H:%M', time_stamp, 'unixepoch') as visit_time_stamp, count(*) as visit_count from posts_analytics where post_id = ? GROUP BY visit_time_stamp ORDER BY visit_time_stamp ASC"""
        parameter = (post_id,)
    else:
        time_delta_args = {"weeks": weeks or 0, "days": days or 0, "hours": hours}

        user_query_limit = int(
            (datetime.now() - timedelta(**time_delta_args)).timestamp()
        )

        sql_query = """select strftime('%Y-%m-%d %H:%M', time_stamp, 'unixepoch') as visit_time_stamp, count(*) as visit_count from posts_analytics where post_id = ? and time_stamp > ? GROUP BY visit_time_stamp ORDER BY visit_time_stamp ASC"""
        parameter = (post_id, user_query_limit)

    try:
        Log.database(f"Connecting to '{Settings.DB_ANALYTICS_ROOT}' database")

        connection = sqlite3.connect(Settings.DB_ANALYTICS_ROOT)
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()

        cursor.execute(sql_query, parameter)
        post_traffic_data = cursor.fetchall()

        js_time_stamp_and_count = [
            [
                int((datetime.strptime(entry[0], "%Y-%m-%d %H:%M")).timestamp() * 1000),
                entry[1],
            ]
            for entry in post_traffic_data
        ]

        connection.close()

        return js_time_stamp_and_count
    except Exception:
        Log.error(f"Failed to retrieve traffic data for post analytics: {post_id}")
        return []


def get_analytics_page_os_graph_data(post_id: int) -> dict:
    """
    Returns the post's visitors os data list of tuples.
    Args:
        `post_id` (int): The post's primary key/id whose visitors operating system counts data to be retrived.

    Returns:
        `dict`: os_name_list: e.g. ["Windows", "Mac", "Android"...]. , os_count_list: e.g. [3445, 6756, 53453, ...]
    """

    try:
        Log.database(f"Connecting to '{Settings.DB_ANALYTICS_ROOT}' database")

        connection = sqlite3.connect(Settings.DB_ANALYTICS_ROOT)
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()

        cursor.execute(
            """select os as os_name, count(*) as os_count from posts_analytics where post_id = ? GROUP BY os""",
            (post_id,),
        )
        post_graph_os_data = cursor.fetchall() or []

        os_graph_data = {
            "os_name_list": [os[0] for os in post_graph_os_data],
            "os_count_list": [counts[1] for counts in post_graph_os_data],
        }
        connection.close()

        return os_graph_data
    except Exception:
        Log.error(f"Failed to retrieve os data for post analytics: {post_id}")
        return {"os_name_list": [], "os_count_list": []}


def get_analytics_page_country_graph_data(post_id: int, view_all=False) -> dict:
    """
    Returns the post's visitors traffic data list of tuples.
    Args:
        `post_id` (int): The post's primary key/id whose visitors country data to be retrieved.
        `view_all` (bool):
            - True: Returns all data since the post was created.
            - False: Returns only the latest 25 data entries.

    Returns:
        `dict`: country_name_list: e.g. ["Russia", "Germany"...]. , country_count_list: e.g. [3445, 6756, ...]
    """

    if view_all:
        sql_query = """select country as country_name, count(*) as country_count from posts_analytics where post_id = ? GROUP BY country ORDER BY country_count DESC"""
    else:
        sql_query = """select country as country_name, count(*) as country_count from posts_analytics where post_id = ? GROUP BY country ORDER BY country_count DESC limit 25"""

    try:
        Log.database(f"Connecting to '{Settings.DB_ANALYTICS_ROOT}' database")

        connection = sqlite3.connect(Settings.DB_ANALYTICS_ROOT)
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()

        cursor.execute(sql_query, (post_id,))
        post_country_data = cursor.fetchall()

        country_graph_data = {
            "country_name_list": [country[0] for country in post_country_data],
            "country_count_list": [counts[1] for counts in post_country_data],
        }

        connection.close()

        return country_graph_data
    except Exception:
        Log.error(f"Failed to retrieve country data for post analytics: {post_id}")
        return {
            "country_name_list": [],
            "country_count_list": [],
        }
