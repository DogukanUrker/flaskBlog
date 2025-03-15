# Import the necessary modules and functions
from modules import (
    ANALYTICS,  # Constants to check analytics feature
    DB_ANALYTICS_ROOT,  # Path to the analytics database
    Blueprint,  # Blueprint for defining routes
    Log,  # Custom logging module
    getAnalyticsPageCountryGraphData,  # Function to get post country graph data
    getAnalyticsPageTrafficGraphData,  # Function to get post traffic graph data
    make_response,  # Function to make http response
    request,  # Request handling module
    session,  # Session management module
    sqlite3,  # SQLite database module
)

# Create a blueprint for the return posts analytics graph data route
returnPostAnalyticsDataBlueprint = Blueprint("returnPostTrafficGraphData", __name__)


@returnPostAnalyticsDataBlueprint.route("/api/v1/postTrafficGraphData")
def returnPostTrafficGraphData() -> dict:
    """
    Retrieves traffic graph data for a given post.

    This API fetches traffic analytics for a specific post, allowing filtering based on
    the time since the post was published.

    Args (Query Parameters):
        if None of below kwargs are given then default will be last 48 hours data
        - `postID` (int, required): The ID of the post for which traffic data is requested.
        - `sincePosted` (bool, optional): If `True`, fetches data since the post was published and other kwargs will be ignored.
        - `weeks` (float, optional): Number of weeks to filter the traffic data.
        - `days` (float, optional): Number of days to filter the traffic data.
        - `hours` (float, optional): Number of hours to filter the traffic data.

    Returns:
        - `200 OK`: Successfully retrieves graph data.
        - `403 Forbidden`: If the client is not authenticated.
        - `404 Not Found`: If `postID` is missing.
        - `410 Gone`: If analytics is disabled by the admin.
    """
    # Accept postID type integer
    postID = request.args.get("postID", type=int)
    # Accept True or False and convert into boolean, default to False
    sincePosted = str(request.args.get("sincePosted", default=False)).lower()=="true"
    # Accept weeks type float
    weeks = request.args.get("weeks", type=float, default=0)
    # Accept days type float
    days = request.args.get("days", type=float, default=0)
    # Accept hours type float
    hours = request.args.get("hours", type=float, default=0)

    # Check if analytics is true or false by admin for flaskblog
    match ANALYTICS:
        case True:
            # Ensure the user is authenticated
            match "userName" in session:
                case True:
                    if postID:
                        # Fetch and return traffic graph data for the post
                        return make_response(
                            {
                                "payload": getAnalyticsPageTrafficGraphData(
                                    postID=postID,
                                    sincePosted=sincePosted,
                                    weeks=weeks,
                                    days=days,
                                    hours=hours,
                                )
                            },
                            200,
                        )
                    else:
                        # Return error if postID is missing
                        return make_response(
                            {
                                "message": "Missing postID; unable to retrieve data.",
                                "error": "postID (type: int) is required.",
                            },
                            404,
                        )

                case False:
                    # Return forbidden error if the user is not authenticated
                    return make_response(
                        {
                            "message": "client don't have permission",
                            "error": "request denied",
                        },
                        403,
                    )
        case False:
            # Return error if analytics is disabled
            return ({"message": "analytics is disabled by admin"}, 410)


# api end point for country graph data
@returnPostAnalyticsDataBlueprint.route("/api/v1/postCountryGraphData")
def returnPostCountryGraphData() -> dict:
    """
    Retrieves country-based graph data for a given post.

    This API returns country-wise analytics data for a specific post ID,
    providing insights into the geographical distribution of viewers.

    Args (Query Parameters):
        `postID` (int, required): The ID of the post for which analytics data is requested.
        `viewAll` (bool, optional): If `True`, returns data for all time; otherwise, return top 25 countries.

    Returns:
        `200 OK`: Successfully retrieves graph data.
        `403 Forbidden`: If the client is not authenticated.
        `404 Not Found`: If `postID` is missing.
        `410 Gone`: If analytics is disabled by the admin.
    """
    # Accept postID
    postID = request.args.get("postID", type=int)
    # Accept True or False and convert into boolean, default to False
    viewAll = str(request.args.get("viewAll", default=False)).lower()=="true"

    # Check if analytics is true or false by admin for flaskblog
    match ANALYTICS:
        case True:
            match "userName" in session:
                case True:
                    if postID:
                        # Fetch and return country graph data for the post
                        return make_response(
                            {
                                "payload": getAnalyticsPageCountryGraphData(
                                    postID=postID, viewAll=viewAll
                                )
                            },
                            200,
                        )
                    else:
                        # Return error if postID is missing
                        return make_response({"message" : "Missing postID; unable to retrieve data.", "error" : "postID (type: int) is required."}, 404)
                        
                case False:
                    # Return forbidden error if the user is not authenticated
                    return make_response(
                        {
                            "message": "client don't have permission",
                            "error": "request denied",
                        },
                        403,
                    )
        case False:
            # Return error if analytics is disabled
            return make_response({"message": "analytics is disabled by admin"}, 410)


# api for storing visitors time spend duration
@returnPostAnalyticsDataBlueprint.route("/api/v1/timeSpendsDuration", methods={"POST"})
def storeTimeSpendsDuraton() -> dict:
    """
    This function stores the time spent by a visitor on a post.

    This API updates the `timeSpendDuration` field in the `postsAnalytics` table
    for a given visitor.

    Request Data (JSON):
        `visitorID (int)`: Unique identifier of the visitor.
        `spendTime (int)`: Time spent (in seconds).

    Returns:
        `200 OK`: If the update is successful.
        `500 Internal Server Error`: If an error occurs.
        `405 Method Not Allowed`: If an unsupported HTTP method is used.
    """

    # Check if analytics is true or false by admin for flaskblog
    match ANALYTICS:
        case True:
            # Handle POST requests
            match request.method == "POST":
                case True:
                    visitorData = request.json
                    visitorID = visitorData.get("visitorID")
                    spendTime = visitorData.get("spendTime")

                    try:
                        # Connect to the posts database
                        connection = sqlite3.connect(DB_ANALYTICS_ROOT)
                        connection.set_trace_callback(
                            Log.database
                        )  # Set the trace callback for the connection
                        cursor = connection.cursor()

                        # Update the time spend duration with the new data
                        cursor.execute(
                            """update postsAnalytics set timeSpendDuration = ? where id = ? """,
                            (spendTime, visitorID),
                        )
                        connection.commit()
                        return make_response({"message": "Successfully upadated"}, 200)
                    except:
                        # Return internal server error
                        return make_response(
                            {"message": "Unexpected error occured"}, 500
                        )

                case False:
                    # Return method not allowed
                    return make_response({"message": "Method not allowed"}, 405)

        case False:
            # Return error if analytics is disabled
            return ({"message": "analytics is disabled by admin"}, 410)
