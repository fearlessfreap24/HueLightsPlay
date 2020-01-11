import requests
import os
import time
from dotenv import load_dotenv
from flask import Flask,redirect

# read .env file to get Hue Key
load_dotenv()

# read HUEKEY environmental variable
hk = os.getenv("HUEKEY")
hip = os.getenv("HUEIP")

app = Flask(__name__)

def getLights():
    # create base url
    url = "http://"+hip+"/api/"+hk

    # getting lights data
    r = requests.get(url+"/lights")

    # turn lights JSON into a dict for reading
    dict = r.json()

    light = "<table><tr><th>Number</th><th>Name</th><th>State</th></tr>"
    for i in dict:
        light = light + "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(i, dict[i]['name'], dict[i]['state']['on'])
    light = light + "</table><p><a href=\"./dylan\">Turn on/off my light</a></p>"
    return light

@app.route('/')
def index():
	return 'Index Page'

@app.route('/hello/')
def hello():
	return 'Hello World'

@app.route('/lights')
def lights():
    return getLights()

@app.route('/dylan')
def dylan():
	light5 = requests.get("http://" + hip + "/api/" + hk + "/lights/5/")
	control5 = light5.json()
	currStatus = control5['state']['on']
	url = "http://" + hip + "/api/" + hk
	requests.put(url+"/lights/5/state", json={'on': not currStatus})
	return redirect("./lights")
