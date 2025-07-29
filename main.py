import requests, json, csv
import pandas as pd

if not os.path.exists('./output'):
    os.mkdir('./output')
    
def get_data():
    url = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
    response = requests.get(url,
                            params={
                                'format' : 'geojson',
                                'starttime' : '2024-01-01 00:00:00','endtime' : '2025-07-28 23:59:59',
                                'minmagnitude' : 2, 'maxmagnitude' : 10,
                                'minlongitude' : -125, 'maxlongitude' : -65,
                                'minlatitude' : 24, 'maxlatitude' : 50,
                                'eventtype' : 'earthquake',
                                'limit': 100
                            },)
    return response.json()

def save_json(data, filename='earthquakes.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved JSON to {filename}")

def convert_to_csv(json_data, csv_filename='earthquakes.csv'):
    # Flatten the list of features
    records = []
    for feature in json_data['features']:
        props = feature['properties']
        coords = feature['geometry']['coordinates']
        records.append({
            'id': feature['id'],
            'magnitude': props.get('mag'),
            'place': props.get('place'),
            'time': props.get('time'),
            'updated': props.get('updated'),
            'tz': props.get('tz'),
            'url': props.get('url'),
            'felt': props.get('felt'),
            'alert': props.get('alert'),
            'longitude': coords[0],
            'latitude': coords[1],
            'depth': coords[2],
        })
    
    df = pd.DataFrame(records)
    df.to_csv(csv_filename, index=False, encoding='utf-8')
    print(f"Saved CSV to {csv_filename}")

# Run everything
data = get_data()
save_json(data, 'earthquakes.json')
convert_to_csv(data, 'earthquakes.csv')
