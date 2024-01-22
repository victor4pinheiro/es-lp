from es_lp.utils import config
from elasticsearch import Elasticsearch

client = Elasticsearch(
    "https://localhost:9200/",
    api_key=config.ELASTIC_API,
    ca_certs=config.ELASTIC_CA_CERTS,
)
