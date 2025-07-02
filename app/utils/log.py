"""
This module contains the code for the Log variable.
"""

from os import mkdir
from os.path import exists

from settings import Settings
from tamga import Tamga

if not exists(Settings.LOG_FOLDER_ROOT):
    mkdir(Settings.LOG_FOLDER_ROOT)

Log = Tamga(
    logToFile=Settings.LOG_TO_FILE,
    logToConsole=Settings.TAMGA_LOGGER,
    logFile=Settings.LOG_FILE_ROOT,
)
