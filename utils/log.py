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
"""

# Import necessary modules
from modules import (
    mkdir,  # Importing the mkdir function from modules
    exists,  # Importing the exists function from modules
    APP_NAME,  # Importing the application name configuration
    APP_VERSION,  # Importing the application version configuration
    currentTime,  # Importing the currentTime function from modules
    currentDate,  # Importing the currentDate function from modules
    BREAKER_TEXT,  # Importing the BREAKER_TEXT variable from modules
    CUSTOM_LOGGER,  # Importing the custom logger configuration
    LOG_FILE_ROOT,  # Importing the LOG_FILE_ROOT variable from modules
    currentTimeZone,  # Importing the currentTimeZone function from modules
    LOG_FOLDER_ROOT,  # Importing the LOG_FOLDER_ROOT variable from modules
    LOG_APP_FILE_ROOT,  # Importing the LOG_APP_FILE_ROOT variable from modules
    LOG_SQL_FILE_ROOT,  # Importing the LOG_SQL_FILE_ROOT variable from modules
    LOG_INFO_FILE_ROOT,  # Importing the LOG_INFO_FILE_ROOT variable from modules
    LOG_DANGER_FILE_ROOT,  # Importing the LOG_DANGER_FILE_ROOT variable from modules
    LOG_SUCCESS_FILE_ROOT,  # Importing the LOG_SUCCESS_FILE_ROOT variable from modules
    LOG_WARNING_FILE_ROOT,  # Importing the LOG_WARNING_FILE_ROOT variable from modules
)

# Checking if LOG_FOLDER_ROOT directory exists
match exists(LOG_FOLDER_ROOT):
    case False:  # If LOG_FOLDER_ROOT doesn't exist
        mkdir(LOG_FOLDER_ROOT)  # Create LOG_FOLDER_ROOT directory


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
        # Match CUSTOM_LOGGER status
        match CUSTOM_LOGGER:
            case True:
                # Print formatted danger message with timestamp
                print(
                    f"\033[38;2;244;63;94m{APP_NAME}@{APP_VERSION}\033[0m"  # Log app name and version in rose-500
                    "\033[38;2;115;115;115m[\033[0m"  # Open the square brackets in neutral-500
                    f"\033[38;2;217;70;239m{currentDate()}\033[0m"  # Print current date in indigo-500
                    "\033[38;2;115;115;115m |\033[0m"  # Print vertical line in neutral-500
                    f"\033[38;2;236;72;153m {currentTime(seconds=True)}\033[0m"  # Print current time in violet-500
                    "\033[38;2;115;115;115m |\033[0m"  # Print vertical line in neutral-500
                    f"\033[38;2;168;85;247m {currentTimeZone()}\033[0m"  # Print current time zone in purple-500
                    "\033[38;2;115;115;115m] \033[0m"  # Close the square brackets in neutral-500
                    "\033[38;2;220;38;38m"  # Set text color to red-600
                    "\033[48;2;248;113;113m"  # Set background color to red-400
                    "\033[1m DANGER \033[0m"  # Print "DANGER" in bold red-600
                    "\033[0m"  # Reset color
                    "\033[0m"  # Reset color
                    f"\033[38;2;239;68;68m {message}\033[0m\n"  # Print the danger message in red-500
                )
                # Open log file in append mode and write the formatted message
                logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
                logFile.write(
                    f"[{currentDate()}"  # Write current date
                    f"|{currentTime(seconds=True,microSeconds=True)}"  # Write current time with microseconds
                    f"|{currentTimeZone()}]"  # Write current time zone
                    "\t"  # Separate fields with tab
                    f"DANGER | {message}\n"  # Write the danger message
                )
                logFile.close()  # Close the log file
                # Open danger log file in append mode and write the formatted message
                logDangerFile = open(LOG_DANGER_FILE_ROOT, "a", encoding="utf-8")
                logDangerFile.write(
                    f"[{currentDate()}"  # Write current date
                    f"|{currentTime(seconds=True,microSeconds=True)}"  # Write current time with microseconds
                    f"|{currentTimeZone()}]"  # Write current time zone
                    "\t"  # Separate fields with tab
                    f"{message}\n"  # Write the danger message
                )
                logDangerFile.close()  # Close the danger log file

    # Define a method to log success messages
    def success(message: str = "NONE") -> None:
        """
        Logs a success message with a timestamp to the console and to a log file.

        Args:
            message (str, optional): The message to log. Defaults to "NONE".

        Returns:
            None: None
        """
        # Match CUSTOM_LOGGER status
        match CUSTOM_LOGGER:
            case True:
                # Print formatted success message with timestamp
                print(
                    f"\033[38;2;244;63;94m{APP_NAME}@{APP_VERSION}\033[0m"  # Log app name and version in rose-500
                    "\033[38;2;115;115;115m[\033[0m"  # Open the square brackets in neutral-500
                    f"\033[38;2;217;70;239m{currentDate()}\033[0m"  # Print current date in indigo-500
                    "\033[38;2;115;115;115m |\033[0m"  # Print vertical line in neutral-500
                    f"\033[38;2;236;72;153m {currentTime(seconds=True)}\033[0m"  # Print current time in violet-500
                    "\033[38;2;115;115;115m |\033[0m"  # Print vertical line in neutral-500
                    f"\033[38;2;168;85;247m {currentTimeZone()}\033[0m"  # Print current time zone in purple-500
                    "\033[38;2;115;115;115m] \033[0m"  # Close the square brackets in neutral-500
                    "\033[38;2;22;163;74m"  # Set text color to green-600
                    "\033[48;2;74;222;128m"  # Set background color to green-400
                    "\033[1m SUCCESS \033[0m"  # Print "SUCCESS" in bold green-600
                    "\033[0m"  # Reset color
                    "\033[0m"  # Reset color
                    f"\033[38;2;34;197;94m {message}\033[0m\n"  # Print the success message in green-500
                )
                # Open log file in append mode and write the formatted message
                logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
                logFile.write(
                    f"[{currentDate()}"  # Write current date
                    f"|{currentTime(seconds=True,microSeconds=True)}"  # Write current time with microseconds
                    f"|{currentTimeZone()}]"  # Write current time zone
                    "\t"  # Separate fields with tab
                    f"SUCCESS | {message}\n"  # Write the success message
                )
                logFile.close()  # Close the log file
                # Open success log file in append mode and write the formatted message
                logSuccessFile = open(LOG_SUCCESS_FILE_ROOT, "a", encoding="utf-8")
                logSuccessFile.write(
                    f"[{currentDate()}"  # Write current date
                    f"|{currentTime(seconds=True,microSeconds=True)}"  # Write current time with microseconds
                    f"|{currentTimeZone()}]"  # Write current time zone
                    "\t"  # Separate fields with tab
                    f"{message}\n"  # Write the success message
                )
                logSuccessFile.close()  # Close the success log file

    # Define a method to log warning messages
    def warning(message: str = "NONE") -> None:
        """
        Logs a warning message with a timestamp to the console and to a log file.

        Args:
            message (str, optional): The message to log. Defaults to "NONE".

        Returns:
            None: None
        """
        # Match CUSTOM_LOGGER status
        match CUSTOM_LOGGER:
            case True:
                # Print formatted warning message with timestamp
                print(
                    f"\033[38;2;244;63;94m{APP_NAME}@{APP_VERSION}\033[0m"  # Log app name and version in rose-500
                    "\033[38;2;115;115;115m[\033[0m"  # Open the square brackets in neutral-500
                    f"\033[38;2;217;70;239m{currentDate()}\033[0m"  # Print current date in indigo-500
                    "\033[38;2;115;115;115m |\033[0m"  # Print vertical line in neutral-500
                    f"\033[38;2;236;72;153m {currentTime(seconds=True)}\033[0m"  # Print current time in violet-500
                    "\033[38;2;115;115;115m |\033[0m"  # Print vertical line in neutral-500
                    f"\033[38;2;168;85;247m {currentTimeZone()}\033[0m"  # Print current time zone in purple-500
                    "\033[38;2;115;115;115m] \033[0m"  # Close the square brackets in neutral-500
                    "\033[38;2;234;88;12m"  # Set text color to orange-600
                    "\033[48;2;251;146;60m"  # Set background color to orange-400
                    "\033[1m WARNING \033[0m"  # Print "WARNING" in bold orange-600
                    "\033[0m"  # Reset color
                    "\033[0m"  # Reset color
                    f"\033[38;2;249;115;22m {message}\033[0m\n"  # Print the warning message in orange-500
                )
                # Open log file in append mode and write the formatted message
                logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
                logFile.write(
                    f"[{currentDate()}"  # Write current date
                    f"|{currentTime(seconds=True,microSeconds=True)}"  # Write current time with microseconds
                    f"|{currentTimeZone()}]"  # Write current time zone
                    "\t"  # Separate fields with tab
                    f"WARNING | {message}\n"  # Write the warning message
                )
                logFile.close()  # Close the log file
                # Open warning log file in append mode and write the formatted message
                logWarningFile = open(LOG_WARNING_FILE_ROOT, "a", encoding="utf-8")
                logWarningFile.write(
                    f"[{currentDate()}"  # Write current date
                    f"|{currentTime(seconds=True,microSeconds=True)}"  # Write current time with microseconds
                    f"|{currentTimeZone()}]"  # Write current time zone
                    "\t"  # Separate fields with tab
                    f"{message}\n"  # Write the warning message
                )
                logWarningFile.close()  # Close the warning log file

    # Define a method to log info messages
    def info(message: str = "NONE") -> None:
        """
        Logs a info message with a timestamp to the console and to a log file.

        Args:
            message (str, optional): The message to log. Defaults to "NONE".

        Returns:
            None: None
        """
        # Match CUSTOM_LOGGER status
        match CUSTOM_LOGGER:
            case True:
                # Print formatted info message with timestamp
                print(
                    f"\033[38;2;244;63;94m{APP_NAME}@{APP_VERSION}\033[0m"  # Log app name and version in rose-500
                    "\033[38;2;115;115;115m[\033[0m"  # Open the square brackets in neutral-500
                    f"\033[38;2;217;70;239m{currentDate()}\033[0m"  # Print current date in indigo-500
                    "\033[38;2;115;115;115m |\033[0m"  # Print vertical line in neutral-500
                    f"\033[38;2;236;72;153m {currentTime(seconds=True)}\033[0m"  # Print current time in violet-500
                    "\033[38;2;115;115;115m |\033[0m"  # Print vertical line in neutral-500
                    f"\033[38;2;168;85;247m {currentTimeZone()}\033[0m"  # Print current time zone in purple-500
                    "\033[38;2;115;115;115m] \033[0m"  # Close the square brackets in neutral-500
                    "\033[38;2;37;99;235m"  # Set text color to blue-600
                    "\033[48;2;96;165;250m"  # Set background color to blue-400
                    "\033[1m INFO \033[0m"  # Print "INFO" in bold blue-600
                    "\033[0m"  # Reset color
                    "\033[0m"  # Reset color
                    f"\033[38;2;59;130;246m {message}\033[0m\n"  # Print the info message in blue-500
                )
                # Open log file in append mode and write the formatted message
                logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
                logFile.write(
                    f"[{currentDate()}"  # Write current date
                    f"|{currentTime(seconds=True,microSeconds=True)}"  # Write current time with microseconds
                    f"|{currentTimeZone()}]"  # Write current time zone
                    "\t"  # Separate fields with tab
                    f"INFO | {message}\n"  # Write the info message
                )
                logFile.close()  # Close the log file
                # Open info log file in append mode and write the formatted message
                logInfoFile = open(LOG_INFO_FILE_ROOT, "a", encoding="utf-8")
                logInfoFile.write(
                    f"[{currentDate()}"  # Write current date
                    f"|{currentTime(seconds=True,microSeconds=True)}"  # Write current time with microseconds
                    f"|{currentTimeZone()}]"  # Write current time zone
                    "\t"  # Separate fields with tab
                    f"{message}\n"  # Write the info message
                )
                logInfoFile.close()  # Close the info log file

    # Define a method to log app messages
    def app(message: str = "NONE") -> None:
        """
        Logs a app message with a timestamp to the console and to a log file.

        Args:
            message (str, optional): The message to log. Defaults to "NONE".

        Returns:
            None: None
        """
        # Match CUSTOM_LOGGER status
        match CUSTOM_LOGGER:
            case True:
                # Print formatted app message with timestamp
                print(
                    f"\033[38;2;244;63;94m{APP_NAME}@{APP_VERSION}\033[0m"  # Log app name and version in rose-500
                    "\033[38;2;115;115;115m[\033[0m"  # Open the square brackets in neutral-500
                    f"\033[38;2;217;70;239m{currentDate()}\033[0m"  # Print current date in indigo-500
                    "\033[38;2;115;115;115m |\033[0m"  # Print vertical line in neutral-500
                    f"\033[38;2;236;72;153m {currentTime(seconds=True)}\033[0m"  # Print current time in violet-500
                    "\033[38;2;115;115;115m |\033[0m"  # Print vertical line in neutral-500
                    f"\033[38;2;168;85;247m {currentTimeZone()}\033[0m"  # Print current time zone in purple-500
                    "\033[38;2;115;115;115m] \033[0m"  # Close the square brackets in neutral-500
                    "\033[38;2;8;145;178m"  # Set text color to sky-600
                    "\033[48;2;32;211;238m"  # Set background color to sky-400
                    "\033[1m APP \033[0m"  # Print "APP" in bold sky-600
                    "\033[0m"  # Reset color
                    "\033[0m"  # Reset color
                    f"\033[38;2;6;182;212m {message}\033[0m\n"  # Print the sql message in sky-500
                )
                # Open log file in append mode and write the formatted message
                logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
                logFile.write(
                    f"[{currentDate()}"  # Write current date
                    f"|{currentTime(seconds=True,microSeconds=True)}"  # Write current time with microseconds
                    f"|{currentTimeZone()}]"  # Write current time zone
                    "\t"  # Separate fields with tab
                    f"APP | {message}\n"  # Write the app message
                )
                logFile.close()  # Close the log file
                # Open app log file in append mode and write the formatted message
                logAppFile = open(LOG_APP_FILE_ROOT, "a", encoding="utf-8")
                logAppFile.write(
                    f"[{currentDate()}"  # Write current date
                    f"|{currentTime(seconds=True,microSeconds=True)}"  # Write current time with microseconds
                    f"|{currentTimeZone()}]"  # Write current time zone
                    "\t"  # Separate fields with tab
                    f"{message}\n"  # Write the app message
                )
                logAppFile.close()  # Close the app log file

    # Define a method to log sql messages
    def sql(message: str = "NONE") -> None:
        """
        Logs a sql message with a timestamp to the console and to a log file.

        Args:
            message (str, optional): The message to log. Defaults to "NONE".

        Returns:
            None: None
        """
        # Match CUSTOM_LOGGER status
        match CUSTOM_LOGGER:
            case True:
                # Print formatted sql message with timestamp
                print(
                    f"\033[38;2;244;63;94m{APP_NAME}@{APP_VERSION}\033[0m"  # Log app name and version in rose-500
                    "\033[38;2;115;115;115m[\033[0m"  # Open the square brackets in neutral-500
                    f"\033[38;2;217;70;239m{currentDate()}\033[0m"  # Print current date in indigo-500
                    "\033[38;2;115;115;115m |\033[0m"  # Print vertical line in neutral-500
                    f"\033[38;2;236;72;153m {currentTime(seconds=True)}\033[0m"  # Print current time in violet-500
                    "\033[38;2;115;115;115m |\033[0m"  # Print vertical line in neutral-500
                    f"\033[38;2;168;85;247m {currentTimeZone()}\033[0m"  # Print current time zone in purple-500
                    "\033[38;2;115;115;115m] \033[0m"  # Close the square brackets in neutral-500
                    "\033[38;2;13;148;136m"  # Set text color to teal-600
                    "\033[48;2;45;212;191m"  # Set background color to teal-400
                    "\033[1m SQL \033[0m"  # Print "SQL" in bold teal-600
                    "\033[0m"  # Reset color
                    "\033[0m"  # Reset color
                    f"\033[38;2;20;184;166m {message}\033[0m\n"  # Print the app message in teal-500
                )
                # Open log file in append mode and write the formatted message
                logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
                logFile.write(
                    f"[{currentDate()}"  # Write current date
                    f"|{currentTime(seconds=True,microSeconds=True)}"  # Write current time with microseconds
                    f"|{currentTimeZone()}]"  # Write current time zone
                    "\t"  # Separate fields with tab
                    f"SQL | {message}\n"  # Write the sql message
                )
                logFile.close()  # Close the log file
                # Open SQL log file in append mode and write the formatted message
                logSQLFile = open(LOG_SQL_FILE_ROOT, "a", encoding="utf-8")
                logSQLFile.write(
                    f"[{currentDate()}"  # Write current date
                    f"|{currentTime(seconds=True,microSeconds=True)}"  # Write current time with microseconds
                    f"|{currentTimeZone()}]"  # Write current time zone
                    "\t"  # Separate fields with tab
                    f"{message}\n"  # Write the sql message
                )
                logSQLFile.close()  # Close the sql log file

    # Define a method to print a breaker line
    def breaker():
        """
        Prints a breaker to the console and appends the line to the log file.

        Returns:
            None: None
        """
        # Match CUSTOM_LOGGER status
        match CUSTOM_LOGGER:
            case True:
                # Print breaker line
                print(
                    f"\033[38;2;115;155;155m{BREAKER_TEXT}\033[0m"
                )  # Set text color to neutral-500
                # Open log file in append mode and write the breaker line
                logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
                logFile.write(BREAKER_TEXT + "\n")
                logFile.close()  # Close the log file
