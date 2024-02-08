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

Log.breaker: This method prints a breaker line (a line with dashes) to the console and appends the breaker line to the log file.

Note: The code is written in Python 3.12, and the docstrings follow the PEP 257 style guide.
"""

# Import necessary modules
from modules import (
    currentTime,  # Importing currentTime function from modules
    currentDate,  # Importing currentDate function from modules
    BREAKER_TEXT,  # Importing BREAKER_TEXT variable from modules
    LOG_FILE_ROOT,  # Importing LOG_FILE_ROOT variable from modules
    currentTimeZone,  # Importing currentTimeZone function from modules
    LOG_APP_FILE_ROOT,  # Importing LOG_APP_FILE_ROOT variable from modules
    LOG_INFO_FILE_ROOT,  # Importing LOG_INFO_FILE_ROOT variable from modules
    LOG_DANGER_FILE_ROOT,  # Importing LOG_DANGER_FILE_ROOT variable from modules
    LOG_SUCCESS_FILE_ROOT,  # Importing LOG_SUCCESS_FILE_ROOT variable from modules
    LOG_WARNING_FILE_ROOT,  # Importing LOG_WARNING_FILE_ROOT variable from modules
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
        # Print formatted danger message with timestamp
        print(
            f"\n\033[94m[{currentDate()}\033[0m"  # Print current date in cyan
            f"\033[95m {currentTime(seconds=True)}\033[0m"  # Print current time in magenta
            f"\033[94m {currentTimeZone()}] \033[0m"  # Print current time zone in cyan
            "\033[90m" # Set text color to black
            "\033[101m"  # Set background color to red
            "\033[1m DANGER \033[0m"  # Print "DANGER:" in bold red
            "\033[0m"  # Reset color
            "\033[0m"  # Reset color
            f"\033[91m {message}\033[0m\n"  # Print the danger message in red
        )
        # Open log file in append mode and write the formatted message
        logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
        logFile.write(
            f"[{currentDate()}"  # Write current date
            f"|{currentTime(seconds=True,microSeconds=True)}"  # Write current time with microseconds
            f"|{currentTimeZone()}]"  # Write current time zone
            "\t"  # Separate fields with tab
            f"DANGER: {message}\n"  # Write the danger message
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
        # Print formatted success message with timestamp
        print(
            f"\n\033[94m[{currentDate()}\033[0m"  # Print current date in cyan
            f"\033[95m {currentTime(seconds=True)}\033[0m"  # Print current time in magenta
            f"\033[94m {currentTimeZone()}] \033[0m"  # Print current time zone in cyan
            "\033[90m" # Set text color to black
            "\033[102m"  # Set background color to green
            "\033[1m SUCCESS \033[0m"  # Print "SUCCESS:" in bold green
            "\033[0m"  # Reset color
            "\033[0m"  # Reset color
            f"\033[92m {message}\033[0m\n"  # Print the success message in green
        )
        # Open log file in append mode and write the formatted message
        logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
        logFile.write(
            f"[{currentDate()}"  # Write current date
            f"|{currentTime(seconds=True,microSeconds=True)}"  # Write current time with microseconds
            f"|{currentTimeZone()}]"  # Write current time zone
            "\t"  # Separate fields with tab
            f"SUCCESS: {message}\n"  # Write the success message
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
        # Print formatted warning message with timestamp
        print(
            f"\n\033[94m[{currentDate()}\033[0m"  # Print current date in cyan
            f"\033[95m {currentTime(seconds=True)}\033[0m"  # Print current time in magenta
            f"\033[94m {currentTimeZone()}] \033[0m"  # Print current time zone in cyan
            "\033[90m" # Set text color to black
            "\033[103m"  # Set background color to yellow
            "\033[1m WARNING \033[0m"  # Print "WARNING:" in bold yellow
            "\033[0m"  # Reset color
            "\033[0m"  # Reset color
            f"\033[93m {message}\033[0m\n"  # Print the warning message in yellow
        )
        # Open log file in append mode and write the formatted message
        logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
        logFile.write(
            f"[{currentDate()}"  # Write current date
            f"|{currentTime(seconds=True,microSeconds=True)}"  # Write current time with microseconds
            f"|{currentTimeZone()}]"  # Write current time zone
            "\t"  # Separate fields with tab
            f"WARNING: {message}\n"  # Write the warning message
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
        # Print formatted info message with timestamp
        print(
            f"\n\033[94m[{currentDate()}\033[0m"  # Print current date in cyan
            f"\033[95m {currentTime(seconds=True)}\033[0m"  # Print current time in magenta
            f"\033[94m {currentTimeZone()}] \033[0m"  # Print current time zone in cyan
            "\033[90m" # Set text color to black
            "\033[106m"  # Set background color to cyan
            "\033[1m INFO \033[0m"  # Print "INFO:" in bold cyan
            "\033[0m"  # Reset color
            "\033[0m"  # Reset color
            f"\033[96m {message}\033[0m\n"  # Print the info message in cyan
        )
        # Open log file in append mode and write the formatted message
        logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
        logFile.write(
            f"[{currentDate()}"  # Write current date
            f"|{currentTime(seconds=True,microSeconds=True)}"  # Write current time with microseconds
            f"|{currentTimeZone()}]"  # Write current time zone
            "\t"  # Separate fields with tab
            f"INFO: {message}\n"  # Write the info message
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
        # Print formatted app message with timestamp
        print(
            f"\n\033[94m[{currentDate()}\033[0m"  # Print current date in pink
            f"\033[95m {currentTime(seconds=True)}\033[0m"  # Print current time in magenta
            f"\033[94m {currentTimeZone()}] \033[0m"  # Print current time zone in pink
            "\033[90m" # Set text color to black
            "\033[105m"  # Set background color to pink
            "\033[1m APP \033[0m"  # Print "APP:" in bold pink
            "\033[0m"  # Reset color
            "\033[0m"  # Reset color
            f"\033[95m {message}\033[0m\n"  # Print the app message in pink
        )
        # Open log file in append mode and write the formatted message
        logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
        logFile.write(
            f"[{currentDate()}"  # Write current date
            f"|{currentTime(seconds=True,microSeconds=True)}"  # Write current time with microseconds
            f"|{currentTimeZone()}]"  # Write current time zone
            "\t"  # Separate fields with tab
            f"APP: {message}\n"  # Write the app message
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

    # Define a method to print a breaker line
    def breaker():
        """
        Prints a breaker to the console and appends the line to the log file.

        Returns:
            None: None
        """
        # Print breaker line
        print(f"\033[90m {BREAKER_TEXT}\033[0m")
        # Open log file in append mode and write the breaker line
        logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
        logFile.write(BREAKER_TEXT + "\n")
        logFile.close()  # Close the log file
