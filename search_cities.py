import urllib.request as urllib2
import json
from math import cos

def search_cities(lat, long, numelts):
    # determine extent to which road travel may reach in ~500 miles, dependent on current latitude
    dlat = 7.24637681159
    dlong = dlat/cos(lat)
    url_range = "http://api.geonames.org/citiesJSON?north={}&south={}&east={}&west={}&maxRows={}&username=free".format(lat+dlat, lat-dlat, long-dlong, long+dlong, numelts)
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
    print(search_cities(40.8262, -73.5021, 500))
