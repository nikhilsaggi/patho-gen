import urllib.request as urllib2
import json
from math import cos, radians

def search_cities_dist(lat, long, numelts, api_key):
    ## Currently not in use because Google APIs are expensive ##
    # determine extent to which road travel may reach in ~500 miles, dependent on current latitude
    dlat = 7.24637681159
    dlong = dlat/cos(radians(lat))
    url_range = "http://api.geonames.org/citiesJSON?north={}&south={}&east={}&west={}&maxRows={}&username=free".format(lat+dlat, lat-dlat, long-dlong, long+dlong, numelts)
    # access city api. Data is obtained from GeoNames Geographical Database.
    with urllib2.urlopen(url_range) as url:
        data = json.loads(url.read().decode())
    list_cities = []
    try:
        for city in data['geonames']:
            # ensure city is within 8 hours by driving. Data is obtained from Google Distance Matrix API.
            url_dist = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={},{}&destinations={},{}&key={}".format(lat, long, city['lat'], city['lng'], api_key)
            with urllib2.urlopen(url_dist) as url2:
                if json.loads(url2.read().decode())['rows'][0]['elements'][0]['duration']['value'] < 28800:
                    # record latitude, longitude and population for each city reached
                    list_cities.append((city['lat'], city['lng'], city['population']))
    # if api times out, the request is retried with a fewer number of cities
    except KeyError:
        return(search_cities(lat, long, int(numelts*0.8)))
    return(list_cities)

def search_cities(lat, long, numelts):
    # determine extent to which road travel may reach in ~500 miles, dependent on current latitude
    dlat = 7.24637681159
    dlong = dlat/cos(radians(lat))
    url_range = "http://api.geonames.org/citiesJSON?north={}&south={}&east={}&west={}&maxRows={}&username=free".format(lat+dlat, lat-dlat, long+dlong, long-dlong, numelts)
    # access city api. Data is obtained from GeoNames Geographical Database.
    with urllib2.urlopen(url_range) as url:
        data = json.loads(url.read().decode())
    list_cities = []
    # record latitude, longitude and population for each city reached
    try:
        for city in data['geonames']:
            list_cities.append((city['lat'], city['lng'], city['population']))
    # if api times out, the request is retried with a fewer number of cities
    except KeyError:
        return(search_cities(lat, long, int(numelts*0.8)))
    return(list_cities)

if __name__ == '__main__':
    print(search_cities(40.8262, -73.5021, 100))
