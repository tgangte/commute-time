import requests
import time
from elasticsearch import Elasticsearch
from datetime import datetime
from pytz import timezone
# Author: Thanglalson Gangte
# 14/04/2017
# Collect daily commute time from work to home using Google Directions API 
#Insert the data into elasticsearch and plot graphs using Kibana or any charting laibrary of your choice


mtz = timezone('UTC')
_time = datetime.now(mtz)
human_time = _time.strftime('%Y-%m-%d %H:%M:%S')

current_time = int(time.time())


# login to google account and get api_key from here
# https://developers.google.com/maps/documentation/directions/get-api-key
api_key = 'asdd653ghg1fvGy2L0xfYnuadsadsjhjhas675'
es = Elasticsearch(['localhost'], port=9200)  # elasticsearch hostname and port
base_url = 'https://maps.googleapis.com/maps/api/directions/json'

# the two addresses as given in google maps
home = "Garuda Mall, Magrath Road, Craig Park Layout, Ashok Nagar, Bengaluru, Karnataka"
work = "Global%20Technology%20Park,%20Tower%20A,%20Global%20Technology%20park%20-%20Entrance%20Road,%20Service%20Road,%20Bellandur,%20Bengaluru,%20Karnataka%20560103"


def getCommuteDetails(origin, destination, which_way):
    r = requests.get(base_url + "?origin=" + origin + "&destination=" + destination +
                     "&traffic_mode=best_guess&departure_time=" + str(current_time) + "&key=" + api_key)
    distance = r.json()['routes'][0]['legs'][0]['distance']
    duration = r.json()['routes'][0]['legs'][0]['duration']
    duration_in_traffic = r.json()['routes'][0]['legs'][
        0]['duration_in_traffic']
    start_address = r.json()['routes'][0]['legs'][0]['start_address']
    end_address = r.json()['routes'][0]['legs'][0]['end_address']
    doc = {
        "duration_seconds":  duration['value'],
        "duration_text": duration['text'],
        "duration_in_traffic_seconds": duration_in_traffic['value'],
        "duration_in_traffic": duration_in_traffic['text'],

        "distance_meters": distance['value'],
        "distance_text":  distance["text"],
        "timestamp": human_time,
        "start_address": start_address,
        "end_address": end_address,
        "which_way": which_way,


    }

    res = es.index(index="commute1", doc_type='mytype',
                   body=doc)  # insert to elasticsearch

    print "Inserted the following data to elk "
    print doc

# to be run every 5 or 10 minutes with cron
getCommuteDetails(work, home, "work to home")

# to be run every 5 or 10 minutes with cron
getCommuteDetails(home, work, "home to work")
