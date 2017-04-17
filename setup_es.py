from elasticsearch import Elasticsearch

# set elasticsearch endpoint(s) here
es_hosts, index, doctype = ['localhost:9200'], 'commute1', 'mytype'

# index settings and mappings
settings = {'index': {'number_of_shards': 3, 'number_of_replicas': 0}}
mappings = {
    doctype: {
        'properties': {
            'timestamp': { 'type': 'date', 'format': 'yyyy-MM-dd HH:mm:s', 'store': True },
            'start_address': { 'type': 'string', 'store': True },
            'end_address': { 'type': 'string', 'store': True },

            'distance_meters': { 'type': 'long', 'store': True },
            'distance_meters': { 'type': 'string', 'store': True },

            'duration_seconds': { 'type': 'long', 'store': True },
            'duration_text': { 'type': 'string', 'store': True },

            'duration_in_traffic_seconds': { 'type': 'long', 'store': True },
            'duration_in_traffic': { 'type': 'string', 'store': True },
        }
    }
}

# create the index
body = { 'settings': settings, 'mappings': mappings }
Elasticsearch(es_hosts).indices.create(index=index, body=body)
print 'Index', index, 'created'
