from es_lp.config import environments
from elasticsearch import Elasticsearch

client = Elasticsearch(
    "https://localhost:9200/",
    api_key=environments.ELASTIC_API,
    ca_certs=environments.ELASTIC_CA_CERTS,
)
