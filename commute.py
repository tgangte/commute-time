from datetime import datetime
import requests

from elasticsearch import Elasticsearch

# Author: Thanglalson Gangte
# 14/04/2017
# Collect daily commute time from work to home using Google Directions API
# Insert the data into elasticsearch and plot graphs using Kibana or any charting tool of your choice

### INPUT SECTION ###

# login to google account and get api_key from here
# https://developers.google.com/maps/documentation/directions/get-api-key
api_key = '<insert_yours_here>'
# set elasticsearch endpoint(s) here
es_hosts, index, doctype = ['localhost:9200'], 'commute1', 'mytype'
# the two addresses as given in google maps
home = "Garuda Mall, Magrath Road, Craig Park Layout, Ashok Nagar, Bengaluru, Karnataka"
work = "Global Technology Park, Tower A, Global Technology park - Entrance Road, Service Road, Bellandur, Bengaluru, Karnataka 560103"

### END OF INPUT ###

# use a single source of truth on current time
now = datetime.utcnow()
epoch = int((now - datetime(1970, 1, 1)).total_seconds())
es_time = now.strftime('%Y-%m-%d %H:%M:%S')

# elasticsearch connection
es = Elasticsearch(es_hosts)

base_url = 'https://maps.googleapis.com/maps/api/directions/json'

for origin, destination in [(home, work), (work, home)]:
    params = {
        "origin": origin,
        "destination": destination,
        "traffic_mode": 'best_guess',
        "departure_time": epoch,
        "key": api_key,
    }
    data = requests.get(base_url, params=params).json()['routes'][0]['legs'][0]

    distance, duration, duration_in_traffic = data['distance'], data['duration'], data['duration_in_traffic']
    doc = {
        "timestamp": es_time,
        "start_address": data['start_address'],
        "end_address": data['end_address'],

        "distance_meters": distance['value'],
        "distance_text": distance['text'],

        "duration_seconds": duration['value'],
        "duration_text": duration['text'],

        "duration_in_traffic_seconds": duration_in_traffic['value'],
        "duration_in_traffic": duration_in_traffic['text'],
    }

    res = es.index(index=index, doc_type=doctype, body=doc)  # insert to elasticsearch

    print "Inserted the following data to elk "
    print res
