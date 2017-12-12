from requests import get
import json
from pprint import pprint

url = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getallstations'

stations = get(url).json()['items']

station = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getlatestmeasurements/534382'

weather = get(station).json()['items']
pprint(weather)
