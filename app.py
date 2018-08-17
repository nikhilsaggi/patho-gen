from flask import Flask, flash, redirect, render_template, request, session, abort
import main
import json

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
    result = eval(request.form['affectedCities'])
    explored = json.loads(request.form['savedLocs'])
    # use inputted coordinates if this is the first execution
    if result == []:
        result = [(lat, long)]
        print("new")
    # determine affected cities in the next cycle
    result, explored = main.simulate(result, rate, explored)
    explored = json.dumps(explored)
    return render_template('layout_map.html', **locals())

if __name__ == "__main__":
    app.run()
