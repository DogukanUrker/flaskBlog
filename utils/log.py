from modules import (
    BREAKER_TEXT,
    LOG_FILE_ROOT,
    currentDate,
    currentTime,
    currentTimeZone,
)


# Function to print messages with color and log them
def message(
    color="0",
    message="NO MESSAGE CONTENT",
    breaker=False,
):
    """
    Prints a colored message to the console and appends it to the log file. The color parameter can be any number between 0 and 9, where 0 is the default color and 9 is the brightest color. The breaker parameter can be set to True to print a line breaker before the message.
    """
    match breaker:
        case True:
            # Print line breaker with specified color code
            print(f"\033[9{color}m {BREAKER_TEXT}\033[0m")
            # Append line breaker to log file
            logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
            logFile.write(BREAKER_TEXT + "\n")
            logFile.close()
        case False:
            # Print message with timestamp and color code
            print(
                f"\n\033[94m[{currentDate()}\033[0m"
                f"\033[95m {currentTime(seconds=True)}\033[0m"
                f"\033[94m {currentTimeZone()}] \033[0m"
                f"\033[9{color}m {message}\033[0m\n"
            )
            # Append message to log file with timestamp
            logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
            logFile.write(
                f"[{currentDate()}"
                f"|{currentTime(seconds=True,microSeconds=True)}"
                f"|{currentTimeZone()}]"
                "\t"
                f"{message}\n"
            )
            logFile.close()
