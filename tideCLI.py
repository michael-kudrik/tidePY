import argparse
import datetime
import requests

STATIONS = { # list of stations. used when running help
    "Montauk": 8510560,
    "Kings Point": 8516945,
    "The Battery": 8518750,
    "Sandy Hook": 8531680,
    "Atlantic City": 8534720,
    "Cape May": 8536110,
    "Block Island": 8459338,
    "Newport": 8452660,
    "Providence": 8454000,
    "Quonset Point": 8454049,
    "Conimicut Light": 8452944
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("location", nargs="?", help="Name of the tide location")
    parser.add_argument("-f","--fetch", action="store_true", help="fetches tide")
    parser.add_argument("-l","--list", action="store_true", help="displays list of available tide locations")
    args=parser.parse_args()
    location_name = args.location
    station_id = STATIONS.get(location_name)

    if args.fetch:
            tide_data = fetchTideData(station_id, interval='hilo')
    elif args.list:
           print("\n\nNEW YORK:\nMontauk - 8510560\nKings Point - 8516945\nThe Battery - 8518750\n\nNEW JERSEY:\nSandy Hook - 8531680\nAtlantic City - 8534720\nCape May - 8536110\n\nRHODE ISLAND:\nBlock Island - 8459338\nNewport - 8452660\nProvidence - 8454000\nQuonset Point - 8454049\nConimicut Light - 8452944\n\n")
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
    # right now it is set to just do current. might implement a way to toggle between the two in the future
    today = datetime.datetime.now().strftime("%Y%m%d")
   # tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y%m%d")
    
    params = {
        'begin_date': today,
        'end_date': today, #change this if you want future predictions
        'station': station_id,  # Station (duh)
        'product': product,     # 'predictions'
        'datum': 'STND',        # Standard datum
        'time_zone': 'lst_ldt', # Local time w/ daylight saving
        'interval': interval,   # 'hilo' = only high/low
        'units': 'english',     # Feet
        'format': 'json'        # JSON response
    }
    
    # usefull for debugging
    print(f"Fetching data for station ID: {station_id}")
    #print(f"API URL: {base_url}")
    #print(f"Parameters: {params}")

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()

    if 'predictions' in data:
        return data['predictions']  
    else:
        print("No tide data available for this buoy.")
        return None

def format(tide_data):
        bars = "▁▂▃▄▅▆▇█"
        values = [float(entry.get('v')) for entry in tide_data]
        max_height = max(values) if values else 1
        min_height = min(values) if values else 0
        # Identify the two lowest and two highest tide values
        sorted_values = sorted(values)
        low_tides = set(sorted_values[:2])
        high_tides = set(sorted_values[-2:])
        for entry in tide_data:
                time_str = entry.get('t')
                value = float(entry.get('v'))
                try:
                        dt = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
                        formatted_time = dt.strftime("%b %d, %Y %I:%M %p")
                except Exception:
                        formatted_time = time_str
                index = int((value / max_height) * (len(bars)-1))
                bar_char = bars[index]
                output = f"{formatted_time:<20} | {value:>5.2f} ft {bar_char*10}"
                if value in low_tides:
                        print(f"\033[94m{output}\033[0m\n")  # Blue for low tide
                elif value in high_tides:
                        print(f"\033[91m{output}\033[0m\n")  # Red for high tide
                else:
                        print(f"{output}\n")
                

# tidePy.fetchTideData()

if __name__ == "__main__":
      main()