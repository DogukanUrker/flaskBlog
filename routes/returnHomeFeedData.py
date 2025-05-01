# Import required modules and functions
from modules import (
    getHomeFeedData,
    Blueprint,
    make_response,
    getSlugFromPostTitle,
    url_for,
    getProfilePicture,
    request,
    datetime,
)

returnHomeFeedDataBlueprint = Blueprint("returnHomeFeedData", __name__)


@returnHomeFeedDataBlueprint.route("/api/v1/homeFeedData")
def homeFeedData():
    """
    API endpoint to fetch home feed data.
    Accepts query parameters: category, by, sort, limit, offset
    """

    # Get query parameters with default values if not provided
    category = request.args.get("category", type=str, default="all")
    by = request.args.get("by", type=str, default="hot")
    sort = request.args.get("sort", type=str, default="desc")
    limit = request.args.get("limit", type=int, default=6)
    offset = request.args.get("offset", type=int, default=0)

    try:
        # Fetch raw home feed data based on parameters
        rawHomeFeedData = getHomeFeedData(
            category=category, by=by, sort=sort, limit=limit, offset=offset
        )

        listOfHomeFeedData = []

        # Process each post's raw data
        for data in rawHomeFeedData:
            homeFeedObj = {}
            homeFeedObj["id"] = data[0]  # Post ID
            homeFeedObj["title"] = data[1]  # Post Title
            homeFeedObj["content"] = data[2]  # Post Content
            homeFeedObj["author"] = data[3]  # Author Name
            homeFeedObj["timeStamp"] = datetime.fromtimestamp(data[4]).strftime(
                "%d.%m.%y"
            )  # Timestamp
            homeFeedObj["category"] = data[5]  # Post Category
            homeFeedObj["urlID"] = data[6]  # URL ID

            # Generate URL for the post's banner image
            homeFeedObj["bannerImgSrc"] = url_for(
                "returnPostBanner.returnPostBanner", postID=data[0]
            )

            # Get the author's profile picture
            homeFeedObj["authorProfile"] = getProfilePicture(data[3])

            # Generate URL for viewing the full post
            homeFeedObj["postLink"] = url_for(
                "post.post", slug=getSlugFromPostTitle(data[1]), urlID=data[6]
            )

            # Add the processed post data to the list
            listOfHomeFeedData.append(homeFeedObj)

        # Return the list as a JSON payload with status 200 OK
        return make_response({"payload": listOfHomeFeedData}, 200)

    except Exception as e:
        # In case of any error, return a JSON error response with status 500 Internal Server Error
        return make_response({"error": f"{e}"}, 500)
