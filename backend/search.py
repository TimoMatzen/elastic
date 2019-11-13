from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

HEADERS = {'content-type': 'application/json'}


def search(term: str):
    client = Elasticsearch()

    docs = 'Insert your search term'

    # Elasticsearch 6 requires the content-type header to be set, and this is
    # not included by default in the current version of elasticsearch-py
    client.transport.connection_pool.connection.headers.update(HEADERS)

    s = Search(using=client)
    name_query = {'query': {term}}
    if term:
        docs = s.query("query_string", query=term).execute()

    return docs
