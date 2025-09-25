import argparse
import datetime
import requests

STATIONS = {
    "Montauk": {"id": 8510560, "state": "NY"},
    "Kings Point": {"id": 8516945, "state": "NY"},
    "The Battery": {"id": 8518750, "state": "NY"},
    "Sandy Hook": {"id": 8531680, "state": "NJ"},
    "Atlantic City": {"id": 8534720, "state": "NJ"},
    "Cape May": {"id": 8536110, "state": "NJ"},
    "Block Island": {"id": 8459338, "state": "RI"},
    "Newport": {"id": 8452660, "state": "RI"},
    "Providence": {"id": 8454000, "state": "RI"},
    "Quonset Point": {"id": 8454049, "state": "RI"},
    "Conimicut Light": {"id": 8452944, "state": "RI"},
    "Eastport": {"id": 8410140, "state": "ME"},
    "Cutler Farris Wharf": {"id": 8411060, "state": "ME"},
    "Bar Harbor": {"id": 8413320, "state": "ME"},
    "Portland": {"id": 8418150, "state": "ME"},
    "Seavey Island": {"id": 8419870, "state": "ME"},
    "Portland": {"id": 8418150, "state": "ME"},
    "Boston": {"id": 8443970, "state": "MA"},
    "Boston": {"id": 8443970, "state": "MA"},
    "Chatham": {"id": 8447435, "state": "MA"},
    "Nantucket Island": {"id": 8449130, "state": "MA"},
    "Woods Hole": {"id": 8447930, "state": "MA"},
    "New Bedford Harbor": {"id": 8447636, "state": "MA"},
    "Fall River": {"id": 8447386, "state": "MA"},
    "New London": {"id": 8461490, "state": "CT"},
    "New Haven": {"id": 8465705, "state": "CT"},
    "Bridgeport": {"id": 8467150, "state": "CT"},
    "Lewes": {"id": 8557380, "state": "DE"},
    "Ocean City Inlet": {"id": 8570283, "state": "MD"},
    "Bishops Head": {"id": 8571421, "state": "MD"},
    "Cambridge": {"id": 8571892, "state": "MD"},
    "Annapolis": {"id": 8575512, "state": "MD"},
    "Baltimore": {"id": 8574680, "state": "MD"},
    "Chesapeake City": {"id": 8573927, "state": "MD"},
    "Tolchester Beach": {"id": 8573364, "state": "MD"},
    "Solomons Island": {"id": 8577330, "state": "MD"},
    "Washington": {"id": 8594900, "state": "DC"},
    "Washington": {"id": 8594900, "state": "DC"},
    "Dahlgren": {"id": 8635027, "state": "VA"},
    "Lewisetta": {"id": 8635750, "state": "VA"},
    "Windmill Point": {"id": 8636580, "state": "VA"},
    "Wachapreague": {"id": 8631044, "state": "VA"},
    "Kiptopeke": {"id": 8632200, "state": "VA"},
    "Sewells Point": {"id": 8638610, "state": "VA"},
    "Money Point": {"id": 8639348, "state": "VA"},
    "Chesapeake Channel": {"id": 8638901, "state": "VA"},
    "Duck": {"id": 8651370, "state": "NC"},
    "Jennette's Pier": {"id": 8652226, "state": "NC"},
    "Beaufort": {"id": 8656483, "state": "NC"},
    "Oregon Inlet Marina": {"id": 8652587, "state": "NC"},
    "USCG Hatteras": {"id": 8654467, "state": "NC"},
    "Wrightsville Beach": {"id": 8658163, "state": "NC"},
    "Wilmington": {"id": 8658120, "state": "NC"},
    "Springmaid Pier": {"id": 8661070, "state": "SC"},
    "Charleston": {"id": 8665530, "state": "SC"},
    "Fort Pulaski": {"id": 8670870, "state": "GA"},
    "Kings Bay Pier": {"id": 8679598, "state": "GA"},
    "Fernandina Beach": {"id": 8720030, "state": "FL"},
    "Mayport": {"id": 8720218, "state": "FL"},
    "Dames Point": {"id": 8720219, "state": "FL"},
    "St Johns River": {"id": 8720226, "state": "FL"},
    "Port Canaveral": {"id": 8721604, "state": "FL"},
    "Lake Worth Pier": {"id": 8722670, "state": "FL"},
    "South Port Everglades": {"id": 8722956, "state": "FL"},
    "Virginia Key": {"id": 8723214, "state": "FL"},
    "Vaca Key": {"id": 8723970, "state": "FL"},
    "Virginia Key": {"id": 8723214, "state": "FL"},
    "Key West": {"id": 8724580, "state": "FL"},
    "Naples Bay": {"id": 8725114, "state": "FL"},
    "Fort Myers": {"id": 8725520, "state": "FL"},
    "Port Manatee": {"id": 8726384, "state": "FL"},
    "St. Petersburg": {"id": 8726520, "state": "FL"},
    "East Bay": {"id": 8726674, "state": "FL"},
    "Clearwater Beach": {"id": 8726724, "state": "FL"},
    "Cedar Key": {"id": 8727520, "state": "FL"},
    "Apalachicola": {"id": 8728690, "state": "FL"},
    "Panama City": {"id": 8729108, "state": "FL"},
    "Panama City Beach": {"id": 8729210, "state": "FL"},
    "Pensacola": {"id": 8729840, "state": "FL"},

}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("location", nargs="?", help="Name of the tide location")
    parser.add_argument("-f","--fetch", action="store_true", help="fetches tide")
    parser.add_argument("-l","--list", action="store_true", help="displays list of available tide locations")
    args=parser.parse_args()
    location_name = args.location
    station_info = STATIONS.get(location_name)
    station_id = station_info["id"] if station_info else None

    tide_data = None

    if args.fetch:
            tide_data = fetchTideData(station_id, interval='hilo')
    elif args.list:
        print("\nAvailable Tide Locations:\n")
        for name, info in STATIONS.items():
            print(f"{name} ({info['state']}) - {info['id']}")
        print()
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
        max_height = max(values) if values else 1 #provides 1 if list is empty
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
            normalized_value = (value - min_height) / (max_height - min_height) if max_height != min_height else 0
            index = int(normalized_value * (len(bars)-1))
            bar_char = bars[index]
            output = f"{formatted_time:<20} | {value:>5.2f} ft {bar_char*10}"
            if value in low_tides:
                print(f"\033[94m{output}\033[0m\n")  # Blue for low tide
            elif value in high_tides:
                print(f"\033[91m{output}\033[0m\n")  # Red for high tide
            else:
                print(f"{output}\n")
                
if __name__ == "__main__":
      main()