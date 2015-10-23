#!/usr/bin/python
import json
from solongo.estools import store_es
from solongo.rmqtools import get_receiver
from solongo.tools import create_logger


def on_message(channel, method_frame, header_frame, body):
    logger.info('Got Message! Store in ES.')
    logger.debug(json.dumps(body))
    store_es(body)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


logger = create_logger('store-es.log')
logger.info('Store-Es: Start')
queue = 'store_es'
channel = get_receiver(queue, True)
channel.basic_consume(on_message, queue)

try:
    logger.info('Start consuming.')
    channel.start_consuming()
except KeyboardInterrupt:
    channel.close()