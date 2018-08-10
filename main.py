import get_routes
import search_cities
import random

def simulate(cities, rate, explored_cities):
    potential_cities = []
    # find all potentially affected cities
    for lat, long, *rest in cities:
        # check if source cities have already been explored i.e. if the city is in explored_cities
        if (lat, long) in explored_cities.keys():
            potential_cities.extend(explored_cities[(lat, long)])
            continue
        # find all connections using road and flight data
        connections = []
        connections.extend(get_routes.get_routes(lat, long))
        connections.extend(search_cities.search_cities(lat, long, 100))
        potential_cities.extend(connections)
        # update dictionary of explored cities to speed up future searches
        explored_cities[(lat, long)] = connections
    # calculate infection rate from inputted severity (1-10) on a log base 2 scale, ranging from 1 in ~5000 to 1 in 10.
    prob_rate = 2**(10-rate)*10
    # apply infection rate to potential cities
    for city in potential_cities:
        if random.randint(1, prob_rate) == 1:
            cities.append(city)
    return(cities, explored_cities)

if __name__ == '__main__':
    explored = {}
    result1, explored = simulate([(42.4440, -76.5019), (40.8262, -73.5021)], 8, explored)
    print("first iteration: {}".format(result1))
    result2, explored = simulate(result1, 8, explored)
    print("second iteration: {}".format(result2))
