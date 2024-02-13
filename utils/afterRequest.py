# Import the Log and request functions from the modules module
from modules import (
    Log,  # Importing the Log class for logging
    request,  # Module for handling HTTP requests
)


def afterRequestLogger(response):
    """
    This function is used to log the response of an HTTP request.

    Parameters:
        response (Response): The response object returned by the HTTP request.

    Returns:
        Response: The response object returned by the HTTP request.
    """
    # Using a match statement to handle different response statuses
    match response.status:

        # If the response status is "200 OK", log as a success message
        case "200 OK":
            Log.success(
                f"Adress: {request.remote_addr} | Method: {request.method} | Path: {request.path} | Scheme: {request.scheme} | Status: {response.status} | Content Length: {response.content_length} | Referrer: {request.referrer} | User Agent: {request.user_agent}",
            )

        # If the response status is "404 NOT FOUND", log as a danger message
        case "404 NOT FOUND":
            Log.danger(
                f"Adress: {request.remote_addr} | Method: {request.method} | Path: {request.path} | Scheme: {request.scheme} | Status: {response.status} | Content Length: {response.content_length} | Referrer: {request.referrer} | User Agent: {request.user_agent}",
            )

        # For any other response status, log as an info message
        case _:
            Log.info(
                f"Adress: {request.remote_addr} | Method: {request.method} | Path: {request.path} | Scheme: {request.scheme} | Status: {response.status} | Content Length: {response.content_length} | Referrer: {request.referrer} | User Agent: {request.user_agent}",
            )

    return response  # Return the response
