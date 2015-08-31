import json

import pika
from elasticsearch import Elasticsearch


def store_es(ch, method, properties, body):
    print " Empfangen: %r" % (body,)
    es = Elasticsearch([{"host": "sldev", "port": 9200}])
    es.index(index="messages", doc_type="message", body=json.loads(body))


HOST = 'sldev'
CRED = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=HOST, credentials=CRED))

channel = connection.channel()
channel.exchange_declare(exchange='solongo', type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='solongo',
                   queue=queue_name)

print "-- running --"

channel.basic_consume(store_es, queue=queue_name, no_ack=True)
channel.start_consuming()
