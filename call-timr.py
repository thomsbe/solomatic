#!/usr/bin/python

import httplib
import json
import re
import time

from solongo.config import readconfig
from solongo.raspitools import blinkled, GREEN, RED, init_gpio
from solongo.rmqtools import get_receiver
from solongo.tools import create_logger


def on_message(channel, method_frame, header_frame, body):
    message = json.loads(body)
    if message['type'] == 'nfc.uuid.read':
        logger.info('Got message! Call Timr.')
        logger.debug('Message: ' + json.dumps(message))
        conn = httplib.HTTPConnection(server, 80, timeout=5)
        conn.request("GET", uri + message["uuid"])

        r = conn.getresponse()
        if r.status == 200:
            ret = r.getheader('X-Return')
            logger.info('Reply from Timr: ' + ret)
            if re.match('\d', ret) is not None:
                for i in range(0, int(ret)):
                    blinkled(GREEN, 0.05, True)
                    time.sleep(0.1)
            else:
                for i in range(0, 6):
                    blinkled(RED, 0.02, True)
                    time.sleep(0.05)
        else:
            for i in range(0, 7):
                blinkled(RED, 0.02, True)
                time.sleep(0.05)
        conn.close()

    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


config = readconfig()
server = config.get('TIMR', 'server') or 'timr.solongo.office'
uri = config.get('TIMR', 'uri') or '/api/cardreader?id='

logger = create_logger('call-timr.log')
logger.info('Call-Timr: Start')
init_gpio()

queue = 'call-timr'
channel = get_receiver(queue, False)
channel.basic_consume(on_message, queue)

logger.info('Start Consuming.')
channel.start_consuming()
