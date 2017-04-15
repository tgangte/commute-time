curl -XPUT http://localhost:9200/commute1 -H 'Content-Type: application/json' -d '{

 "settings" : {
        "index" : {
            "number_of_shards" : 3,
            "number_of_replicas" : 0
        }
    },
        "mappings": {

                "mytype": {
                        "properties": {
                                "timestamp": {
                                        "type": "date",
                                        "format": "yyyy-MM-dd HH:mm:s",
                                        "store": true


                                },

                                "duration_seconds": {
                                        "type": "long",
                                        "store": true
                                },
                               
                                "which_way": {
                                        "type": "string",
                                       "store": true
                                },
                                "distance_text": {
                                        "type": "string",
                                      "store": true
                                },
                                "duration_in_traffic": {
                                        "type": "string",
                                        "store": true
                                },
                                "duration_in_traffic_seconds": {
                                        "type": "long",
                                       "store": true
                                },
                                "distance_meters": {
                                        "type": "long",
                                        "store": true
                                },
                                "start_address": {
                                        "type": "string",
                                       "store": true

                                },
                                "duration_text": {
                                        "type": "string",
                                        "store": true
                                },
                                "end_address": {
                                        "type": "string",
                                        "store": true
                                }
                        }
                }
        }
}

}'
