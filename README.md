# Smart Meter Electricity Reader

# Description
Smart Meter Electricity Reader (SMER) is a small python application that reads smart meter data from the P1 port of a dutch smart meter and presents the results in a small UI as well as exposes the meter readings via a rest interface. 

## Key remarks
* SMER is not meant to be exposed to the public internet and has no security features whatsoever
* SMER does not automatically persist the read data (altough a manual backup and restore function is available along with a rest interface)
* SMER does not support meters with DSMR < 4.0 but can be easilly adjusted to deal with these meters
* SMER is meant to be run from a raspberry pi, other platforms may require different configuration (especially of the serial interface)
* SMER is a hobby project

## How it works

SMER reads data telegrams from the p1 port of the smart meter and stores the data in memory. The meter reading is available as the current/last reading. every 10 seconds a meter reading is stored in memory and made available via the history endpoint. 

# How to run
Install the required dependencies using pip. A list of the required dependencies can be found in the pip.sh file

Start the application by running 
```
python3 smart_elec_reader.py
```

Navigate with a browser to:
```
http://<ip of your pi>:5000/current-usage
```

# Rest interfaces

SMER exposes a number of rest interfaces for communicating with the web page or for other use
* **GET /api/current**: returns the last meter reading read from the p1 port
* **GET /api/historical?res={resolution}**: returns the last n meter readings where n is the readings that have been stored after _now_ - _resolution (in seconds)_
* **GET /api/store-history**: dumps the readings currently in memory to a history-data.json file one folder up from where the application is run
* **GET /api/load-history**: loads the readings from a history-data.json file located one folder up from where the application is run

# Included resources
SMER includes the following resources that are being served locally by Flask, none of these files have been modified
* Chart.js: https://www.chartjs.org/
* SimpleCSS: https://simplecss.org/

