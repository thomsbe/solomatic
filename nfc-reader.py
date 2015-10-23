#!/usr/bin/python

import json
import time

from solongo.raspitools import RED, init_gpio, init_mifare, get_uid, blinkled, GREEN, piep
from solongo.rmqtools import publish
from solongo.tools import create_logger
from solongo.types import MsgNfc

logger = create_logger('nfc-reader.log')
logger.info("NFC Start")
init_gpio()
mifare = init_mifare()

while True:
    uid = get_uid(mifare, RED, 0.1, logger)
    if uid is not None:
        logger.info("Chip read: " + uid)
        nfc = MsgNfc(uid)
        message = json.dumps(nfc, default=lambda o: o.__dict__)
        logger.info("Publish: " + message)
        blinkled(GREEN, 0.5, True)
        publish(message)
        time.sleep(3)
    time.sleep(1)
