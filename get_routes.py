import urllib.request as urllib2
import io

def get_routes(source_city):
    # fetch airport/route data from urls. Data is obtained from the OpenFlights Airports Database
    http_airports = urllib2.urlopen('https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat')
    http_routes = urllib2.urlopen('https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat')
    # convert airport/route data into readable string lines
    airports = []
    routes = []
    for a in http_airports:
        airports.append(io.BytesIO(a).read().decode("utf-8"))
    http_airports.close()
    for r in http_routes:
        routes.append(io.BytesIO(r).read().decode("utf-8"))
    http_routes.close()
    # obtain source airport(s) from the source city
    source_airports = list(line.split(',')[4][1:-1] for line in airports if line.split(',')[2][1:-1] == source_city)
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
            list_cities.append((line.split(',')[6], line.split(',')[7]))
    return(list_cities)

if __name__ == '__main__':
    print(get_routes("New York"))
