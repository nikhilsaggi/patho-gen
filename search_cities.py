import urllib.request as urllib2
import json

def search_cities(lat, long):
    # set extent to which road travel may reach. Number represents an approximate 8 hour drive within temperate/tropic zones.
    # todo: replace limit with equation based on current latitude
    limit = 6.08
    url_range = "http://api.geonames.org/citiesJSON?north={}&south={}&east={}&west={}&maxRows=500&username=free".format(lat-limit, lat+limit, long+limit, long-limit)
    # access city api. Data is obtained from GeoNames Geographical Database.
    with urllib2.urlopen(url_range) as url:
        data = json.loads(url.read().decode())
        list_cities = []
        # record latitude, longitude and population for each city reached
        try:
            for city in data['geonames']:
                list_cities.append((city['lat'], city['lng'], city['population']))
        except KeyError:
                print("api load failed")
        return(list_cities)

if __name__ == '__main__':
    print(search_cities(40.8262, -73.5021))
