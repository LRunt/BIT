"""
Author: Lukas Runt
Email: lrunt@students.zcu.cz
Date: 16.12.2023
Version: 0.1.0
Description: Logger of the application
"""
import logging


def setup_logger(name, log_file='app.log'):
    """
    Setup of the logger
    :param name: The name of the logger
    :param log_file:The path to the log file (default is 'app.log')
    :return: The configured logger
    """
    logg = logging.getLogger(name)
    logg.setLevel(logging.DEBUG)

    # Create a file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logg.addHandler(file_handler)
    logg.addHandler(console_handler)

    return logg


# Create a logger
logger = setup_logger(__name__)