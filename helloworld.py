import requests
import os
import time
from dotenv import load_dotenv
from flask import Flask,redirect,render_template

# read .env file to get Hue Key
load_dotenv()

# read HUEKEY environmental variable
hk = os.getenv("HUEKEY")
hip = os.getenv("HUEIP")

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/hello/')
def hello():
	return 'Hello World'

@app.route('/lights')
def lights():
    # create base url
    url = "http://"+hip+"/api/"+hk

    # getting lights data
    r = requests.get(url+"/lights")

    # turn lights JSON into a dict for reading
    dict = r.json()
    # render the template and pass dict to template
    return render_template('lights.html', dict=dict)

@app.route('/dylan')
def dylan():
    # request info for light 5
	light5 = requests.get("http://" + hip + "/api/" + hk + "/lights/5/")

	# create dict for reading
	control5 = light5.json()

	# remember the current stae of hte light
	currStatus = control5['state']['on']

	# create base url
	url = "http://" + hip + "/api/" + hk

	# change light state to the opposite of the current state
	requests.put(url+"/lights/5/state", json={'on': not currStatus})

	# return to the lights.html page
	return redirect("./lights")

@app.route('/leopard')
def leopard():

	# create base url
	url = "http://" + hip + "/api/" + hk

	# change light state to the opposite of the current state
	requests.put(url+"/lights/5/state", json={'on': False })
	requests.put(url+"/lights/3/state", json={'on': False })

	# return to the lights.html page
	return redirect("./lights")