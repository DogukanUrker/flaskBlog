"""
This module contains the code for the Log variable.
"""

from os import mkdir
from os.path import exists

from settings import (
    CUSTOM_LOGGER,
    LOG_FILE_ROOT,
    LOG_FOLDER_ROOT,
    LOG_TO_FILE,
)
from tamga import Tamga

if not exists(LOG_FOLDER_ROOT):
    mkdir(LOG_FOLDER_ROOT)

Log = Tamga(logToFile=LOG_TO_FILE, logToConsole=CUSTOM_LOGGER, logFile=LOG_FILE_ROOT)
