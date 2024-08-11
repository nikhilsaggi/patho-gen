from flask import Flask, flash, redirect, render_template, request, session, abort
import main
import ast

app = Flask(__name__)

# default starting page
@app.route("/")
def init():
    return render_template('layout_main.html')

# infection tracking page
@app.route("/map/", methods=['POST'])
def generate():
    # obtain variables passed from html page
    lat = float(request.form['lat'])
    long = float(request.form['long'])
    rate = float(request.form['rate'])
    result = ast.literal_eval(request.form['affectedCities'])
    explored = ast.literal_eval(request.form['savedLocs'])
    # use inputted coordinates if this is the first execution
    if result == []:
        result = [(lat, long)]
    # determine affected cities/routes in the next cycle
    result, explored = main.simulate(result, rate, explored)
    # separate affected routes and cities (for visualization)
    cities_road = [list(city) for city in result if len(city) == 4]
    cities_air = [list(city) for city in result if len(city) == 3]
    # calculate affected population
    population = sum([x[2] for x in cities_road])
    return render_template('layout_map.html', **locals())

if __name__ == "__main__":
    app.run()
