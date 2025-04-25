from modules import (
    getHomeFeedData,
    Blueprint,
    make_response,
    getSlugFromPostTitle,
    url_for,
    getProfilePicture,
    request,
)

returnHomeFeedDataBlueprint = Blueprint("returnHomeFeedData", __name__)


@returnHomeFeedDataBlueprint.route("/api/v1/homeFeedData")
def homeFeedData():
    """
    Takes param parameters
    """
    print(request.args)
    category = request.args.get("category", type=str, default="all")
    by = request.args.get("by", type=str, default="hot")
    sort = request.args.get("sort", type=str, default="desc")
    limit = request.args.get("limit", type=int, default="4")
    offset = request.args.get("offset", type=int, default="0")

    print(category, by, sort, limit, offset, "rohit")

    try:
        rawHomeFeedData = getHomeFeedData(
            category=category, by=by, sort=sort, limit=limit, offset=offset
        )
        listOfHomeFeedData = []
        for data in rawHomeFeedData:
            homeFeedObj = {}
            homeFeedObj["id"] = data[0]
            homeFeedObj["title"] = data[1]
            homeFeedObj["content"] = data[2]
            homeFeedObj["author"] = data[3]
            homeFeedObj["timeStamp"] = data[4]
            homeFeedObj["category"] = data[5]
            homeFeedObj["urlID"] = data[6]
            homeFeedObj["bannerImgSrc"] = url_for(
                "returnPostBanner.returnPostBanner", postID=data[0]
            )
            homeFeedObj["authorProfile"] = getProfilePicture(data[3])
            homeFeedObj["postLink"] = url_for(
                "post.post", slug=getSlugFromPostTitle(data[1]), urlID=data[6]
            )
            listOfHomeFeedData.append(homeFeedObj)

        return make_response({"payload": listOfHomeFeedData}, 200)
    except Exception as e:
        return make_response({"error": f"{e}"}, 500)
