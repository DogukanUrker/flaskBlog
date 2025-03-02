import requests
from user_agents import parse
import geoip2.database

__all__ = ("getDataFromUserIP",)

reader = geoip2.database.Reader("static/geoIP2database/dbip-country-lite-2025-02.mmdb") #path to mmdb file

def userOsInfo(userAgentString) -> str:
    return parse(userAgentString).os.family # return os name string i.e. windows, mac, linux and other os


def getDataFromUserIP(userAgentString : str):
    try:
        userIPAddr = requests.get("https://api.ipify.org", timeout=5)
        response = reader.country(userIPAddr.text.strip())
        return {
            "status": 200,
            "payload":{
                "country": response.country.name,
                "os": userOsInfo(userAgentString),
                "continent": response.continent.name
            }
        }

    except requests.exceptions.RequestException:
        return {"status": 500, "message": "Failed to fetch IP"}
    except geoip2.errors.AddressNotFoundError:
        return {"status": 500, "message": "Invalid IP address"}
    except Exception as e:
        return {"status": 500, "message": f"Unexpected error: {str(e)}"}
    