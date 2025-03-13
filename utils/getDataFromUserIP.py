from modules import database, geoip2, parse, requests

"""
This function will collect user ip using api.ipify.org to fetch user's country, continents
and user Agent string to fetch user oparating system to store post analytics
"""

# geoIP2dabase file needs to be up to date with latests version
# Connect to the geoip2 database
reader = database.Reader(
    "static/geoIP2database/dbip-country-lite-2025-02.mmdb"
)  # path to mmdb file
"""
Free IP geolocation databases
The DB-IP Lite databases are subsets of the commercial databases with reduced
coverage and accuracy. Lite downloads are updated monthly and distributed under
the Creative Commons Attribution License.

Licensing terms
The free DB-IP Lite database by DB-IP is licensed under a Creative Commons Attribution 4.0 International License.

You are free to use this database in your application, provided you give attribution to DB-IP.com for the data.

In the case of a web application, you must include a link back to DB-IP.com on pages that display or use results from the database. You may do it by pasting the HTML code snippet below into your code :

<a href='https://db-ip.com'>IP Geolocation by DB-IP</a>
"""


def getDataFromUserIP(userAgentString: str) -> dict:
    """
    This function returns visitors computer os, country and continent
    Args:
        userAgentString (str): user agent string
    Returns:
        returns dict response containing country name, os, continent or failure message
    """
    try:
        # get visitors ip address by fetching api.ipify.org
        userIPAddr = requests.get("https://api.ipify.org", timeout=5)
        # query in db ip database using visitor's ip address
        response = reader.country(userIPAddr.text.strip())
        # return ip and os data
        return {
            "status": 0,
            "payload": {
                "country": response.country.name,  # get country name from response
                "os": parse(
                    userAgentString
                ).os.family,  # return os name string i.e. windows, mac, linux and other os
                "continent": response.continent.name,  # get continent name from response
            },
        }
    # return error message
    except requests.exceptions.RequestException:
        return {"status": 1, "message": "Failed to fetch IP"}
    except geoip2.errors.AddressNotFoundError:
        return {"status": 1, "message": "Invalid IP address"}
    except Exception as e:
        return {"status": 1, "message": f"Unexpected error: {str(e)}"}
