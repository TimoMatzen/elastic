from elasticsearch import Elasticsearch
from elasticsearch.client import IngestClient

from constants import INDEX_NAME, PIPELINE_ID
from data.data import read_pdf


def main():
    # Connect to localhost:9200 by default.
    es = Elasticsearch()

    # create pipeline
    add_pipeline(es, PIPELINE_ID)

    es.indices.delete(index=INDEX_NAME, ignore=404)
    es.indices.create(
        index=INDEX_NAME,
        body={
            'mappings': {},
            'settings': {},
        },
    )

    pdf = read_pdf('/home/timo/Documenten/artikelen/bayesiaanse netwerken/jury_fallacy.pdf')

    index_pdf(es, pdf)


def add_pipeline(client, PIPELINE_ID):
    # create body pipeline
    body = {
        "description": "parse pdfs and index into ES",
        "processors":
            [
                {"attachment": {"field": "data"}},
            ]
    }

    # use ingest to add pipeline
    ingest = IngestClient(client)
    ingest.put_pipeline(id=PIPELINE_ID, body=body)


def index_pdf(es, body):
    """Add a single pdf to the pdf_index."""

    es.index(index=INDEX_NAME, pipeline=PIPELINE_ID,
             body=body)
    # Don't delete this! You'll need it to see if your indexing job is working,
    # or if it has stalled.
    print("Indexed {}".format("A Great pdf"))


if __name__ == '__main__':
    main()
