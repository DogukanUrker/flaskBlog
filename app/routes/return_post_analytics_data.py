import sqlite3

from flask import Blueprint, make_response, request, session
from settings import Settings
from utils.get_analytics_page_data import (
    get_analytics_page_country_graph_data,
    get_analytics_page_traffic_graph_data,
)
from utils.log import Log

return_post_analytics_data_blueprint = Blueprint(
    "return_post_traffic_graph_data", __name__
)


@return_post_analytics_data_blueprint.route("/api/v1/postTrafficGraphData")
def return_post_traffic_graph_data() -> dict:
    """
    Retrieves traffic graph data for a given post.

    This API fetches traffic analytics for a specific post, allowing filtering based on
    the time since the post was published.

    Args (Query Parameters):
        if None of below kwargs are given then default will be last 48 hours data
        - `post_id` (int, required): The ID of the post for which traffic data is requested.
        - `since_posted` (bool, optional): If `True`, fetches data since the post was published and other kwargs will be ignored.
        - `weeks` (float, optional): Number of weeks to filter the traffic data.
        - `days` (float, optional): Number of days to filter the traffic data.
        - `hours` (float, optional): Number of hours to filter the traffic data.

    Returns:
        - `200 OK`: Successfully retrieves graph data.
        - `403 Forbidden`: If the client is not authenticated.
        - `404 Not Found`: If `post_id` is missing.
        - `410 Gone`: If analytics is disabled by the admin.
    """

    post_id = request.args.get("post_id", type=int)

    since_posted = str(request.args.get("sincePosted", default=False)).lower() == "true"

    weeks = request.args.get("weeks", type=float, default=0)

    days = request.args.get("days", type=float, default=0)

    hours = request.args.get("hours", type=float, default=0)

    if Settings.ANALYTICS:
        if "user_name" in session:
            if post_id:
                return make_response(
                    {
                        "payload": get_analytics_page_traffic_graph_data(
                            post_id=post_id,
                            since_posted=since_posted,
                            weeks=weeks,
                            days=days,
                            hours=hours,
                        )
                    },
                    200,
                )
            else:
                return make_response(
                    {
                        "message": "Missing post_id; unable to retrieve data.",
                        "error": "post_id (type: int) is required.",
                    },
                    404,
                )
        else:
            return make_response(
                {
                    "message": "client don't have permission",
                    "error": "request denied",
                },
                403,
            )
    else:
        return ({"message": "analytics is disabled by admin"}, 410)


@return_post_analytics_data_blueprint.route("/api/v1/postCountryGraphData")
def return_post_country_graph_data() -> dict:
    """
    Retrieves country-based graph data for a given post.

    This API returns country-wise analytics data for a specific post ID,
    providing insights into the geographical distribution of viewers.

    Args (Query Parameters):
        `post_id` (int, required): The ID of the post for which analytics data is requested.
        `view_all` (bool, optional): If `True`, returns data for all time; otherwise, return top 25 countries.

    Returns:
        `200 OK`: Successfully retrieves graph data.
        `403 Forbidden`: If the client is not authenticated.
        `404 Not Found`: If `post_id` is missing.
        `410 Gone`: If analytics is disabled by the admin.
    """

    post_id = request.args.get("post_id", type=int)

    view_all = str(request.args.get("viewAll", default=False)).lower() == "true"

    if Settings.ANALYTICS:
        if "user_name" in session:
            if post_id:
                return make_response(
                    {
                        "payload": get_analytics_page_country_graph_data(
                            post_id=post_id, view_all=view_all
                        )
                    },
                    200,
                )
            else:
                return make_response(
                    {
                        "message": "Missing post_id; unable to retrieve data.",
                        "error": "post_id (type: int) is required.",
                    },
                    404,
                )
        else:
            return make_response(
                {
                    "message": "client don't have permission",
                    "error": "request denied",
                },
                403,
            )
    else:
        return make_response({"message": "analytics is disabled by admin"}, 410)


@return_post_analytics_data_blueprint.route(
    "/api/v1/timeSpendsDuration", methods={"POST"}
)
def store_time_spends_duration() -> dict:
    """
    This function stores the time spent by a visitor on a post.

    This API updates the `time_spend_duration` field in the `posts_analytics` table
    for a given visitor.

    Request Data (JSON):
        `visitor_id (int)`: Unique identifier of the visitor.
        `spend_time (int)`: Time spent (in seconds).

    Returns:
        `200 OK`: If the update is successful.
        `500 Internal Server Error`: If an error occurs.
        `405 Method Not Allowed`: If an unsupported HTTP method is used.
    """

    if Settings.ANALYTICS:
        if request.method == "POST":
            visitor_data = request.json
            visitor_id = visitor_data.get("visitorID")
            spend_time = visitor_data.get("spendTime")

            try:
                connection = sqlite3.connect(Settings.DB_ANALYTICS_ROOT)
                connection.set_trace_callback(Log.database)
                cursor = connection.cursor()

                cursor.execute(
                    """update posts_analytics set time_spend_duration = ? where id = ? """,
                    (spend_time, visitor_id),
                )
                connection.commit()
                return make_response({"message": "Successfully upadated"}, 200)
            except Exception:
                return make_response({"message": "Unexpected error occured"}, 500)
        else:
            return make_response({"message": "Method not allowed"}, 405)
    else:
        return ({"message": "analytics is disabled by admin"}, 410)
