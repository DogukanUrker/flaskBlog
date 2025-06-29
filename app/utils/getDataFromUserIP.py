from geoip2 import database
import geoip2
from user_agents import parse
import requests
import os

"""
This function will collect user ip using api.ipify.org to fetch user's country, continents
and user Agent string to fetch user operating system to store post analytics
"""

# Global variable to hold the reader instance
_reader = None
_reader_initialized = False

def _get_geoip_reader():
    """
    Lazy initialization of the GeoIP database reader.
    Returns None if the database file doesn't exist.
    """
    global _reader, _reader_initialized
    
    if _reader_initialized:
        return _reader
    
    _reader_initialized = True
    db_path = "static/geoIP2database/dbip-country-lite-2025-02.mmdb"
    
    if os.path.exists(db_path):
        try:
            _reader = database.Reader(db_path)
            print(f"GeoIP database loaded successfully from {db_path}")
        except Exception as e:
            print(f"Failed to load GeoIP database: {e}")
            _reader = None
    else:
        print(f"GeoIP database not found at {db_path}. Geographic analytics will be disabled.")
        _reader = None
    
    return _reader

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
        Note: If GeoIP database is not available, country and continent will be "Unknown"
    """
    try:
        # Parse user agent to get OS (this doesn't require GeoIP database)
        user_agent = parse(userAgentString)
        os_name = user_agent.os.family
        
        # Try to get GeoIP reader
        reader = _get_geoip_reader()
        
        if reader is None:
            # GeoIP database is not available, return OS info only
            return {
                "status": 0,
                "payload": {
                    "country": "Unknown",
                    "os": os_name,
                    "continent": "Unknown",
                },
            }
        
        # Get visitor's IP address
        userIPAddr = requests.get("https://api.ipify.org", timeout=5)
        
        # Query GeoIP database using visitor's IP address
        response = reader.country(userIPAddr.text.strip())
        
        # Return IP and OS data
        return {
            "status": 0,
            "payload": {
                "country": response.country.name or "Unknown",
                "os": os_name,
                "continent": response.continent.name or "Unknown",
            },
        }
    
    # Handle various error cases
    except requests.exceptions.RequestException:
        # If IP fetch fails, still return OS info
        try:
            user_agent = parse(userAgentString)
            return {
                "status": 0,
                "payload": {
                    "country": "Unknown",
                    "os": user_agent.os.family,
                    "continent": "Unknown",
                },
            }
        except:
            return {"status": 1, "message": "Failed to fetch IP and parse user agent"}
    
    except geoip2.errors.AddressNotFoundError:
        # IP not found in database, but still return OS info
        try:
            user_agent = parse(userAgentString)
            return {
                "status": 0,
                "payload": {
                    "country": "Unknown",
                    "os": user_agent.os.family,
                    "continent": "Unknown",
                },
            }
        except:
            return {"status": 1, "message": "Invalid IP address"}
    
    except Exception as e:
        # For any other error, try to at least return OS info
        try:
            user_agent = parse(userAgentString)
            return {
                "status": 0,
                "payload": {
                    "country": "Unknown",
                    "os": user_agent.os.family,
                    "continent": "Unknown",
                },
            }
        except:
            return {"status": 1, "message": f"Unexpected error: {str(e)}"}
