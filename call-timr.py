import re
import time
from solongo.config import readconfig
from solongo.raspitools import blinkled, GREEN, RED, init_gpio
from solongo.rmqtools import get_receiver
from solongo.tools import create_logger
import json
import httplib


def on_message(channel, method_frame, header_frame, body):
    message = json.loads(body)
    if message['type'] == 'nfc.uuid.read':
        conn = httplib.HTTPConnection(server, 80, timeout=5)
        conn.request("GET", uri + message["uuid"])

        r = conn.getresponse()
        if r.status == 200:
            ret = r.getheader('X-Return')
            print(ret)
            if re.match('\d', ret) is not None:
                for i in range(0, int(ret)):
                    blinkled(GREEN, 0.1, True)
                    time.sleep(0.2)
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

logger = create_logger()
init_gpio()

queue = 'call-timr'
channel = get_receiver(queue, False)
channel.basic_consume(on_message, queue)

channel.start_consuming()
