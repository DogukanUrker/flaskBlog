import os

import geoip2
import requests
from geoip2 import database
from user_agents import parse

"""
This function will collect user ip using api.ipify.org to fetch user's country, continents
and user Agent string to fetch user operating system to store post analytics
"""


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
        print(
            f"GeoIP database not found at {db_path}. Geographic analytics will be disabled."
        )
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


def get_data_from_user_ip(user_agent_string: str) -> dict:
    """
    This function returns visitors computer os, country and continent
    Args:
        user_agent_string (str): user agent string
    Returns:
        returns dict response containing country name, os, continent or failure message
        Note: If GeoIP database is not available, country and continent will be "Unknown"
    """
    try:
        user_agent = parse(user_agent_string)
        os_name = user_agent.os.family

        reader = _get_geoip_reader()

        if reader is None:
            return {
                "status": 0,
                "payload": {
                    "country": "Unknown",
                    "os": os_name,
                    "continent": "Unknown",
                },
            }

        user_ip_addr = requests.get("https://api.ipify.org", timeout=5)

        response = reader.country(user_ip_addr.text.strip())

        return {
            "status": 0,
            "payload": {
                "country": response.country.name or "Unknown",
                "os": os_name,
                "continent": response.continent.name or "Unknown",
            },
        }

    except requests.exceptions.RequestException:
        try:
            user_agent = parse(user_agent_string)
            return {
                "status": 0,
                "payload": {
                    "country": "Unknown",
                    "os": user_agent.os.family,
                    "continent": "Unknown",
                },
            }
        except Exception:
            return {"status": 1, "message": "Failed to fetch IP and parse user agent"}

    except geoip2.errors.AddressNotFoundError:
        try:
            user_agent = parse(user_agent_string)
            return {
                "status": 0,
                "payload": {
                    "country": "Unknown",
                    "os": user_agent.os.family,
                    "continent": "Unknown",
                },
            }
        except Exception:
            return {"status": 1, "message": "Invalid IP address"}

    except Exception as e:
        try:
            user_agent = parse(user_agent_string)
            return {
                "status": 0,
                "payload": {
                    "country": "Unknown",
                    "os": user_agent.os.family,
                    "continent": "Unknown",
                },
            }
        except Exception:
            return {"status": 1, "message": f"Unexpected error: {str(e)}"}
