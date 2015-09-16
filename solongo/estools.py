import json

from elasticsearch import Elasticsearch

from solongo.config import ReadConfig


def store_es(message):
    config = ReadConfig()

    host = config.get('ES', 'host') or 'localhost'
    port = config.get('ES', 'port') or 9200
    index = config.get('ES', 'index') or 'solomatic'

    es = Elasticsearch([{"host": host, "port": port}])
    es.index(index=index, doc_type="message", body=json.loads(message))
