# commute-time
Record commute time from two distances with Google directions API and store it in Elasticsearch so that it can be visualized in Kibana. 

# Usage
Prequisite: You need to have elasticsearch and kibana setup on your machine.

* Run `sudo pip install -r requirements.txt` to install dependencies
* Run `setup_es.py` - modify any parameters to your liking
* Run `commute.py` to periodically index commute time data in Elasticsearch - insert the required input first


Example:
My office to home is about 6km and takes between 15 to 30 minutes on average, depending on traffic. I have setup the script to run every 2 minutes on cron.
Like so: ```*/2 * * * * /export/apps/python/2.7/bin/python  /home/tgangte/Development/commute_time/commute.py```

After running the script for about 24 hours, the data pattern starts to emerge. The kibana line chart below shows the peak traffic times.

![Alt text](/screenshots/screen1.png?raw=true "Commute time graph on kibana")

