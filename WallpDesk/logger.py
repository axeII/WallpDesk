"""This is Logger model

Makes that everythign is loged to standart output or into specific log file.
"""
__author__ = "ales lerch"

import os
import logging
import datetime

def createLogger(name="default_log",stream=False):

    LOGS_DIR = "~/Desktop/pydesktop_logs"
    FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
    today_date = datetime.datetime.now().strftime("[%Y-%m-%d][%H:%M:%S]")

    def set_file_handler():
        file_name = f"{LOGS_DIR}/{today_date}.log"
        formatter = logging.Formatter(FORMAT,today_date)
        try:
            filehandler = logging.FileHandler(file_name,"w")
        except FileNotFoundError:
            print('[Error] Folder for logging not found!\n[Info] Creating new'
            ' folder...\n[Info] Folder created! Logging now...')
            os.mkdir(LOGS)
            filehandler = logging.FileHandler(file_name,"w")
        filehandler.setLevel(logging.DEBUG)
        filehandler.setFormatter(formatter)
        return filehandler

    def set_stream_handler():
        formatter = logging.Formatter(FORMAT,today_date)
        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(logging.DEBUG)
        streamhandler.setFormatter(formatter)
        return streamhandler

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if stream:
        logger.addHandler(set_stream_handler())
    else:
        logger.addHandler(set_file_handler())

    return logger
