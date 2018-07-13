import urllib.request as urllib2
import io

def get_routes():
    # fetch airport/route data from urls. Data is obtained from the OpenFlights Airports Database
    http_airports = urllib2.urlopen('https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat')
    http_routes = urllib2.urlopen('https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat')
    # covert airport/route data into readable string lines
    airports = []
    routes = []
    for a in http_airports:
        airports.append(io.BytesIO(a).read().decode("utf-8"))
    for r in http_routes:
        routes.append(io.BytesIO(r).read().decode("utf-8"))
    # obtain source airport(s) from inputted source city
    source_city = input("Source city: ")
    source_airports = list(line.split(',')[4][1:-1] for line in airports if line.split(',')[2][1:-1] == source_city)
    if "" in source_airports:
        source_airports.remove("")
    # obtain list of destination airports from source
    list_airports = []
    for airport in source_airports:
        list_airports.extend(line.split(',')[4] for line in routes if line.split(',')[2] == airport)
    # generate list of city names from destination airports
    list_cities = []
    for line in airports:
        if line.split(',')[4][1:-1] in list_airports:
            list_cities.append(line.split(',')[2][1:-1])
    list_cities.sort()
    return(list_cities)

if __name__ == '__main__':
    print(get_routes())
