import sys
import logging

def startLogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    consoleOutputHandler = logging.StreamHandler(sys.stdout)
    consoleOutputHandler.setLevel(logging.INFO)
    log_format = '[%(levelname)s]: %(message)s'
    consoleOutputHandler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(consoleOutputHandler)
