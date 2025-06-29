"""
This module contains the code for the Log variable.
"""

# Import necessary modules
from tamga import Tamga  # Importing Tamga Logger
from os.path import exists  # Importing the exists function
from os import mkdir  # Importing the mkdir function
from constants import (
    CUSTOM_LOGGER,  # Importing the custom logger configuration
    LOG_FILE_ROOT,  # Importing the LOG_FILE_ROOT variable
    LOG_FOLDER_ROOT,  # Importing the LOG_FOLDER_ROOT variable
    LOG_TO_FILE,  # Importing the LOG_TO_FILE variable
)

# Checking if LOG_FOLDER_ROOT directory exists
match exists(LOG_FOLDER_ROOT):
    case False:  # If LOG_FOLDER_ROOT doesn't exist
        mkdir(LOG_FOLDER_ROOT)  # Create LOG_FOLDER_ROOT directory

Log = Tamga(logToFile=LOG_TO_FILE, logToConsole=CUSTOM_LOGGER, logFile=LOG_FILE_ROOT)
