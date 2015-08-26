import pika

from solongo.config import ReadConfig

def publish(message):
    config = ReadConfig()

    host = config.get('RMQ', 'host', 'localhost')
    user = config.get('RMQ', 'user', 'admin')
    passwd = config.get('RMQ', 'passwd', 'admin')
    exchange = config.get('RMQ', 'exchange', 'solongo')

    cred = pika.PlainCredentials(username=user, password=passwd)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=cred))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, type='fanout')

    channel.basic_publish(exchange=exchange, routing_key='', body=message)
    connection.close()
