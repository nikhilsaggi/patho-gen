import urllib.request as urllib2
import io
from math import radians, cos, sin, asin

def get_routes(lat, long):
    # fetch airport/route data from urls and convert airport/route data into readable string lines. Data is obtained from the OpenFlights Airports Database
    with urllib2.urlopen('https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat') as http_airports:
        airports = []
        for a in http_airports:
            airports.append(io.BytesIO(a).read().decode("utf-8"))
    with urllib2.urlopen('https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat') as http_routes:
        routes = []
        for r in http_routes:
            routes.append(io.BytesIO(r).read().decode("utf-8"))
    # obtain source airport(s), if any, near origin coordinates
    source_airports = []
    for line in airports:
        try:
            lat1, long1, lat2, long2 = map(radians, [lat, long, float(line.split(',')[6]), float(line.split(',')[7])])
        # catching a few airports that format incorrectly
        except ValueError:
            continue;
        # using haversine formula, find nearby airports with 75 miles used as max distance
        if 7912 * asin((sin((lat2 - lat1)/2)**2 + cos(lat1) * cos(lat2) * sin((long2 - long1)/2)**2)**0.5) < 75:
            source_airports.append(line.split(',')[4][1:-1])
    if "" in source_airports:
        source_airports.remove("")
    # obtain list of destination airports from source
    list_airports = []
    for airport in source_airports:
        list_airports.extend(line.split(',')[4] for line in routes if line.split(',')[2] == airport)
    # generate list of airport geographic coordinates from destination airports
    list_cities = []
    for line in airports:
        if line.split(',')[4][1:-1] in list_airports:
            list_cities.append((float(line.split(',')[6]), float(line.split(',')[7])))
    return(list_cities)

if __name__ == '__main__':
    print(get_routes(40.7128, -74.0060))
