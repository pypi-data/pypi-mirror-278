import logging
import os

from shining_brain.constants import work_directory


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if logger.hasHandlers():
        logger.handlers.clear()
    file_handler = logging.FileHandler(work_directory + os.sep + '.log')
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formation = '%(asctime)s - %(levelname)s - %(processName)s - ' + '%(threadName)s - %(name)s - %(message)s'
    formatter = logging.Formatter(formation)

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
