import requests
import os
import time
from dotenv import load_dotenv
from flask import Flask

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
    light = light + "</table>"
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

