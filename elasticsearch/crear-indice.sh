#!/bin/bash
curl 'http://localhost:9200/dora' -X PUT -d '{
    "settings" : {
        "index" : {
            "number_of_shards" : 5,
            "number_of_replicas" : 0
        }
    }
}'
