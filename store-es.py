from solongo.estools import store_es
from solongo.rmqtools import get_receiver
from solongo.tools import create_logger


def on_message(channel, method_frame, header_frame, body):
    store_es(body)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


logger = create_logger()

queue = 'store_es'
channel = get_receiver(queue, True)
channel.basic_consume(on_message, queue)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.close()
