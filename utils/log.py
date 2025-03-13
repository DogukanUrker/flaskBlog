"""
This module contains the code for the Log class.

The Log class contains methods to log messages of different types (e.g., danger, success, warning, info) with timestamps. It also contains a method to print a breaker line.

The code is organized as follows:

Imports: The necessary modules are imported.

Define Log class: A Log class is defined, which contains the methods.

Log.danger: This method logs a danger message. It prints a formatted message with timestamp to the console and appends the formatted message to the log file. It also appends the message to the danger log file.

Log.success: This method logs a success message. It prints a formatted message with timestamp to the console and appends the formatted message to the log file. It also appends the message to the success log file.

Log.warning: This method logs a warning message. It prints a formatted message with timestamp to the console and appends the formatted message to the log file. It also appends the message to the warning log file.

Log.info: This method logs an info message. It prints a formatted message with timestamp to the console and appends the formatted message to the log file. It also appends the message to the info log file.

Log.app: This method logs an app message. It prints a formatted message with timestamp to the console and appends the formatted message to the log file. It also appends the message to the app log file.

Log.breaker: This method prints a breaker line (a text in BREAKER_TEXT constant) to the console and appends the breaker line to the log file.

Note: The code is written in Python 3.12, and the docstrings follow the PEP 257 style guide.

Note: Old built-in logger replaced with Tamga Logger (another open-source project by me).
"""

# Import necessary modules
from modules import (
    BREAKER_TEXT,  # Importing the BREAKER_TEXT variable from modules
    CUSTOM_LOGGER,  # Importing the custom logger configuration
    LOG_FILE_ROOT,  # Importing the LOG_FILE_ROOT variable from modules
    LOG_FOLDER_ROOT,  # Importing the LOG_FOLDER_ROOT variable from modules
    Tamga,  # Importing Tamga Logger
    exists,  # Importing the exists function from modules
    mkdir,  # Importing the mkdir function from modules
)

# Checking if LOG_FOLDER_ROOT directory exists
match exists(LOG_FOLDER_ROOT):
    case False:  # If LOG_FOLDER_ROOT doesn't exist
        mkdir(LOG_FOLDER_ROOT)  # Create LOG_FOLDER_ROOT directory

logger = Tamga(
    logToFile=CUSTOM_LOGGER, logToConsole=CUSTOM_LOGGER, logFile=LOG_FILE_ROOT
)


# Define a Log class
class Log:
    # Define a method to log danger messages
    def danger(message: str = "NONE") -> None:
        """
        Logs a danger message with a timestamp to the console and to a log file.

        Args:
            message (str, optional): The message to log. Defaults to "NONE".

        Returns:
            None: None
        """
        logger.error(message)

    # Define a method to log success messages
    def success(message: str = "NONE") -> None:
        """
        Logs a success message with a timestamp to the console and to a log file.

        Args:
            message (str, optional): The message to log. Defaults to "NONE".

        Returns:
            None: None
        """
        logger.success(message)

    # Define a method to log warning messages
    def warning(message: str = "NONE") -> None:
        """
        Logs a warning message with a timestamp to the console and to a log file.

        Args:
            message (str, optional): The message to log. Defaults to "NONE".

        Returns:
            None: None
        """
        logger.warning(message)

    # Define a method to log info messages
    def info(message: str = "NONE") -> None:
        """
        Logs a info message with a timestamp to the console and to a log file.

        Args:
            message (str, optional): The message to log. Defaults to "NONE".

        Returns:
            None: None
        """
        logger.info(message)

    # Define a method to log app messages
    def app(message: str = "NONE") -> None:
        """
        Logs a app message with a timestamp to the console and to a log file.

        Args:
            message (str, optional): The message to log. Defaults to "NONE".

        Returns:
            None: None
        """
        logger.custom(message=message, level="APP", color="blue")

    # Define a method to log sql messages
    def sql(message: str = "NONE") -> None:
        """
        Logs a sql message with a timestamp to the console and to a log file.

        Args:
            message (str, optional): The message to log. Defaults to "NONE".

        Returns:
            None: None
        """
        logger.database(message)

    # Define a method to print a breaker line
    def breaker():
        """
        Prints a breaker to the console and appends the line to the log file.

        Returns:
            None: None
        """
        # Match CUSTOM_LOGGER status
        match CUSTOM_LOGGER and LOG_FILE_ROOT[:-3] != "json":
            case True:
                # Print breaker line
                print(
                    f"\033[38;2;115;155;155m{BREAKER_TEXT}\033[0m"
                )  # Set text color to neutral-500
                # Open log file in append mode and write the breaker line
                logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
                logFile.write(BREAKER_TEXT)
                logFile.close()  # Close the log file
