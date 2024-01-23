from dotenv import load_dotenv
from os import getenv

load_dotenv()

ELASTIC_API = getenv("ELASTIC_API")
ELASTIC_CA_CERTS = getenv("CA_CERTS") or "http_ca.crt"
ELASTIC_USER = getenv("ELASTIC_USER") or "elastic"
ELASTIC_PASSWORD = getenv("ELASTIC_PASSWORD") or "SuperSecret"
