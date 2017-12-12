from requests import get
import json
from pprint import pprint
from haversine import haversine

stations = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getallstations'
weather = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getlatestmeasurements/'

my_lat = 46.8541979
my_lon = -96.8285138

all_stations = get(stations).json()['items']

def find_closest():
    # Longest distance on Earth
    smallest = 20036

    # Get weather station Long/Lat
    for station in all_stations:
        station_lon = station['weather_stn_long']
        station_lat = station['weather_stn_lat']

        # Calculate distance from my location and Long/Lat
        distance = haversine(my_lon, my_lat, station_lon, station_lat)
        
        # Filter list recursively to find shortest distance
        if distance < smallest:
            smallest = distance
            print(station['weather_stn_id'], distance)
            closest_station = station['weather_stn_id']

    return closest_station, distance, my_lon, my_lat, station_lon, station_lat

def find_farthest():
    # Short starting distance
    longest = 1

    for station in all_stations:
        station_lon = station['weather_stn_long']
        station_lat = station['weather_stn_lat']

        # Calculate distance from my location and Long/Lat
        distance = haversine(my_lon, my_lat, station_lon, station_lat)

        # Filter list recursively to find longest distance
        if distance > longest:
            longest = distance
            farthest_station = station['weather_stn_id']

        return farthest_station#, distance, my_lon, my_lat, station_lon, station_lat
