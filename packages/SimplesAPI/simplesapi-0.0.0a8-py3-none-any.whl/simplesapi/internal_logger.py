import logging
import sys


def simplesapi_internal_logger():
    logger = logging.getLogger("SimplesAPI")
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(sys.stdout)
    log_formatter = logging.Formatter("\033[96m%(levelname)s:     %(name)s:\033[0m %(message)s")
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)
    return logger
