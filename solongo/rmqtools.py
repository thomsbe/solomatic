import pika

from solongo.config import readconfig

def publish(message):
    config = readconfig()

    host = config.get('RMQ', 'host') or 'localhost'
    user = config.get('RMQ', 'user')
    passwd = config.get('RMQ', 'passwd')
    exchange = config.get('RMQ', 'exchange')
    vhost = config.get('RMQ', 'vhost')

    cred = pika.PlainCredentials(username=user, password=passwd)
    connection = pika.BlockingConnection(pika.ConnectionParameters(virtual_host=vhost, host=host, credentials=cred))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, type='fanout', durable=True)

    channel.basic_publish(exchange=exchange, routing_key='', body=message)
    connection.close()


def get_receiver(queue, durable):
    config = readconfig()

    host = config.get('RMQ', 'host') or 'localhost'
    user = config.get('RMQ', 'user')
    passwd = config.get('RMQ', 'passwd')
    exchange = config.get('RMQ', 'exchange')
    vhost = config.get('RMQ', 'vhost')

    cred = pika.PlainCredentials(username=user, password=passwd)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, virtual_host=vhost, credentials=cred))
    channel = connection.channel()

    channel.queue_declare(queue=queue, exclusive=True, durable=durable)
    channel.queue_bind(exchange=exchange, queue=queue)

    return channel
