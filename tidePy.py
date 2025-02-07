#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 11:35:58 2025

@author: mikekudrik
"""
import requests

def fetchTideData (station_id, product='predictions', interval='hilo'):
    base_url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
    params = {
        'date': 'recent',  # Fetch recent data
        'station': station_id,
        'product': product,
        'datum': 'STND',  # Standard datum
        'time_zone': 'lst',  # Local standard time
        'interval': interval,  # High/Low tides
        'units': 'english',  # Feet
        'format': 'json'  # JSON response
    } 


    print(f"Fetching data for station ID: {station_id}")
    print(f"API URL: {base_url}")
    print(f"Parameters: {params}")

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()

    if 'predictions' in data:
            return data['predictions']
    else:
        print("No tide data available for this buoy.")
        return None    

tide_data = fetchTideData(1615680, interval='hilo')
for entry in tide_data:
        print(entry)