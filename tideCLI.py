import argparse

import datetime
import requests

def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument("locations", help="list buoy locations")
    parser.add_argument("--fetch", action="store_true", help="fetches tide")
    parser.add_argument("--list", action="store_true", help="displays list of available tide locations")
    args=parser.parse_args()


    tide_data = None
    if args.fetch:
            print("You entered fetch")
            tide_data = fetchTideData(8452660, interval='hilo')
    elif args.list:
           print("\n\nNEW YORK:\nMontauk - 8510560\n\nNEW JERSEY:\nSandy Hook - 8531680\nAtlantic City - 8534720\nCape May - 8536110\n\nRHODE ISLAND:\nBlock Island - 8459338\nNewport - 8452660\nProvidence - 8454000\nQuonset Point - 8454049\nConimicut Light - 8452944\n\n")
    else:
            print("Invalid argument.\nTry again.")
    if tide_data:
            format(tide_data)
    else:
            if args.fetch:
                print("No tide data to format.")


def fetchTideData(station_id, product='predictions', interval='hilo'):
    base_url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
    
    # Get today's date and tomorrow's date (one day ahead)
    today = datetime.datetime.now().strftime("%Y%m%d")
   #tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y%m%d")
    
    params = {
        'begin_date': today,
        'end_date': today,
        'station': station_id,
        'product': product,     # 'predictions'
        'datum': 'STND',        # Standard datum
        'time_zone': 'lst_ldt', # Local time w/ daylight saving
        'interval': interval,   # 'hilo' = only high/low
        'units': 'english',     # Feet
        'format': 'json'        # JSON response
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

def format(tide_data):
        for entry in tide_data:
                # t is time and v is the height of the tide
                time_str = entry.get('t')
                value = entry.get('v')
                try:
                        dt = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
                        formatted_time = dt.strftime("%b %d, %Y %I:%M %p")
                except Exception as e:
                        formatted_time = time_str
                print(f"Time: {formatted_time} | Tide: {value} ft")

# tidePy.fetchTideData()

if __name__ == "__main__":
      main()