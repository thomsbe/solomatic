from solongo.config import readconfig
from solongo.rmqtools import get_receiver
from solongo.tools import create_logger
import json


def on_message(channel, method_frame, header_frame, body):
    message = json.loads(body)
    print message
    print
    if (message['type'] == 'nfc.uuid.read'):
        print message['uuid']
        print
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


config = readconfig()
server = config.get('TIMR', 'server') or 'timr.solongo.office'
uri = config.get('TIMR', 'uri') or '/api/cardreader?id='

logger = create_logger()

queue = 'call-timr'
channel = get_receiver(queue, False)
channel.basic_consume(on_message, queue)

channel.start_consuming()
