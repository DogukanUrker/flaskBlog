from modules import DB_ANALYTICS_ROOT, Log, datetime, sqlite3, timedelta


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
        `list[list[int]]`: if none of params passed except postID function will return last 48 hours data, line grpah data post traffic.
    """

    # Check if none of kwargs are given
    if sincePosted is not True:
        if weeks == 0 and days == 0 and hours == 0:
            # assign defaultt to last 48 hours of data
            hours = 48

    # check if sincePosted is True
    match sincePosted:
        case True:
            # Query the all data since the post was created
            sqlQuery = """select strftime('%Y-%m-%d %H:%M', timeStamp, 'unixepoch') as visitTimeStamp, count(*) as visitCount from postsAnalytics where postID = ? GROUP BY visitTimeStamp ORDER BY visitTimeStamp ASC"""
            parameter = (postID,)
        case False:
            # Construct a dictionary with the time delta arguments, setting default values if None
            timeDeltaArgs = {"weeks": weeks or 0, "days": days or 0, "hours": hours}

            # Calculate the timestamp limit by subtracting the time delta from the current time
            # This converts the adjusted datetime to a Unix timestamp (integer format)
            userQueryLimit = int(
                (datetime.now() - timedelta(**timeDeltaArgs)).timestamp()
            )

            # Query the only selected duration data
            sqlQuery = """select strftime('%Y-%m-%d %H:%M', timeStamp, 'unixepoch') as visitTimeStamp, count(*) as visitCount from postsAnalytics where postID = ? and timeStamp > ? GROUP BY visitTimeStamp ORDER BY visitTimeStamp ASC"""
            parameter = (postID, userQueryLimit)
            # Striping seconds to create rise and fall in line, minute can be stripped too if websites traffic is super high

    try:
        Log.sql(
            f"Connecting to '{DB_ANALYTICS_ROOT}' database"
        )  # Log the database connection is started
        # Use the sqlite3 module to connect to the database and get a cursor object
        connection = sqlite3.connect(DB_ANALYTICS_ROOT)
        connection.set_trace_callback(
            Log.sql
        )  # Set the trace callback for the connection
        cursor = connection.cursor()

        # Execute the query with parameter
        cursor.execute(sqlQuery, parameter)
        postTrafficData = cursor.fetchall()

        # Convert datetime string to javascript millisecond timestamp for apex line chart with views
        jSTimeStampAndCount = [
            [
                int((datetime.strptime(entry[0], "%Y-%m-%d %H:%M")).timestamp() * 1000),
                entry[1],
            ]
            for entry in postTrafficData
        ]

        connection.close()
        # Return proceesed data
        return jSTimeStampAndCount
    except:
        # If traffic data retrieval fails, set empty list and log danger message
        Log.danger(f"Failed to retrieve traffic data for post analytics: {postID}")
        return []  #  return empty list


def getAnalyticsPageOSGraphData(postID: int) -> dict:
    """
    Returns the post's visitors os data list of tuples.
    Args:
        `postID` (int): The post's primary key/id whose visitors operating system counts data to be retrived.

    Returns:
        `dict`: osNameList: e.g. ["Windows", "Mac", "Android"...]. , osCountList: e.g. [3445, 6756, 53453, ...]
    """

    try:
        Log.sql(
            f"Connecting to '{DB_ANALYTICS_ROOT}' database"
        )  # Log the database connection is started
        # Use the sqlite3 module to connect to the database and get a cursor object
        connection = sqlite3.connect(DB_ANALYTICS_ROOT)
        connection.set_trace_callback(
            Log.sql
        )  # Set the trace callback for the connection
        cursor = connection.cursor()
        # Query the os and its counts
        cursor.execute(
            """select os as osName, count(*) as osCount from postsAnalytics where postID = ? GROUP BY os""",
            (postID,),
        )
        postGraphOSData = cursor.fetchall() or []

        # Extract data as osNameList and osCountList
        osGraphData = {
            "osNameList": [os[0] for os in postGraphOSData],
            "osCountList": [counts[1] for counts in postGraphOSData],
        }
        connection.close()

        # Return Process Data
        return osGraphData
    except:
        # If os data retrieval fails, set empty list and log danger message
        Log.danger(f"Failed to retrieve os data for post analytics: {postID}")
        return {"osNameList": [], "osCountList": []}  # return dict with empty data


def getAnalyticsPageCountryGraphData(postID: int, viewAll=False) -> dict:
    """
    Returns the post's visitors traffic data list of tuples.
    Args:
        `postID` (int): The post's primary key/id whose visiors country data to be retrived.
        `viewAll` (bool):
            - True: Returns all data since the post was created.
            - False: Returns only the latest 25 data entries.

    Returns:
        `dict`: osNameList: e.g. ["Russia", "Germany"...]. , osCountList: e.g. [3445, 6756, ...]
    """

    # Check if viewAll is True
    match viewAll:
        case True:
            # Query the all data since post was created
            sqlQuery = """select country as countryName, count(*) as countryCount from postsAnalytics where postID = ? GROUP BY country ORDER BY countryCount DESC"""

        case False:
            # Query the on selected top 25 countries
            sqlQuery = """select country as countryName, count(*) as countryCount from postsAnalytics where postID = ? GROUP BY country ORDER BY countryCount DESC limit 25"""

    try:
        Log.sql(
            f"Connecting to '{DB_ANALYTICS_ROOT}' database"
        )  # Log the database connection is started
        # Use the sqlite3 module to connect to the database and get a cursor object
        connection = sqlite3.connect(DB_ANALYTICS_ROOT)
        connection.set_trace_callback(
            Log.sql
        )  # Set the trace callback for the connection
        cursor = connection.cursor()
        # Execute the query with parameter
        cursor.execute(sqlQuery, (postID,))
        postCountryData = cursor.fetchall()
        # Extract data as countryNameList and countryCountList
        countryGraphData = {
            "countryNameList": [country[0] for country in postCountryData],
            "countryCountList": [counts[1] for counts in postCountryData],
        }

        connection.close()
        # Return Processed data
        return countryGraphData
    except:
        # If country data retrieval fails, set empty list and log danger message
        Log.danger(f"Failed to retrieve country data for post analytics: {postID}")
        return {
            "countryNameList": [],
            "countryCountList": [],
        }  # return dict whih empty list
