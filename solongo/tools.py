import logging
import logging.handlers


def create_logger(filename):
    # LOG_FILENAME = "/var/log/nfc.log"
    LOG_FILENAME = filename
    LOG_LEVEL = logging.INFO

    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LEVEL)

    handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
