from flask import Flask, flash, redirect, render_template, request, session, abort
import main

app = Flask(__name__)

# default starting page
@app.route("/")
def init():
    return render_template('layout_main.html')

# infection tracking page
@app.route("/map/", methods=['POST'])
def generate():
    lat = float(request.form['lat'])
    long = float(request.form['long'])
    rate = float(request.form['rate'])
    explored = {}
    result, dict = main.simulate([(lat, long)], rate, explored)
    return(str(result))

if __name__ == "__main__":
    app.run(debug=True)
