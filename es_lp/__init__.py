from os import getenv
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

ELASTIC_API = getenv("ES_API")
ELASTIC_CA_CERTS = getenv("CA_CERTS") or "http_ca.crt"
ELASTIC_USER = getenv("ELASTIC_USER") or "elastic"
ELASTIC_PASSWORD = getenv("ELASTIC_PASSWORD") or "SuperSecret"

client = Elasticsearch(
    "https://localhost:9200/",
    api_key=ELASTIC_API,
    ca_certs=ELASTIC_CA_CERTS,
    basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
)

client.indices.create(index="my_index")
