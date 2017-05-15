#!/bin/bash
curl 'http://localhost:9200/dbot' -X PUT -d '{
    "settings" : {
        "index" : {
            "number_of_shards" : 5,
            "number_of_replicas" : 0
        }
    }
}'
