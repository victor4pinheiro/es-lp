#!/usr/bin/env sh

if docker container inspect elasticsearch kibana &> /dev/null; then
    docker start elasticsearch kibana
else
    docker compose up -d
    docker cp elasticsearch:/usr/share/elasticsearch/config/certs/http_ca.crt hurl/
    docker cp elasticsearch:/usr/share/elasticsearch/config/certs/http_ca.crt .
fi
