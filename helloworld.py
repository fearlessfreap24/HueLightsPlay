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

# create base url
url = "http://" + hip + "/api/" + hk

headerinfo = {'Home': "/", 'Lights': "/lights", 'Special Functions': "/special", 'Rooms': "/rooms"}

app = Flask(__name__)

# home page
@app.route('/')
def index():
	return render_template("index.html", header=headerinfo)


# test page
@app.route('/hello/')
def hello():
	return 'Hello World'


# display lights and light status
@app.route('/lights')
def lights():

	# getting lights data
    r = requests.get(url+"/lights")

    # turn lights JSON into a dict for reading
    dicto = r.json()

    # render the template and pass dict to template
    return render_template('lights.html', dict=dicto, header=headerinfo)


# function for dylan light on/off
@app.route('/dylan')
def dylan():
    # request info for light 5
	light5 = requests.get(url+"/lights/5/")

	# create dict for reading
	control5 = light5.json()

	# remember the current state of the light
	currStatus = control5['state']['on']

	# change light state to the opposite of the current state
	requests.put(url+"/lights/5/state", json={'on': not currStatus})

	# return to the lights.html page
	return redirect("./lights")


# function to turn off leopard lamp and dylan light
@app.route('/leopard')
def leopard():

	# change light state to off
	requests.put(url+"/lights/5/state", json={'on': False })
	requests.put(url+"/lights/3/state", json={'on': False })

	# return to the lights.html page
	return redirect("./lights")


# a page for links to leopard() and dylan()
@app.route('/special')
def special():

    # render special.html and pass header info
    return render_template("./special.html", header=headerinfo)


# a page to display rooms and rooms stauts
@app.route('/rooms')
def rooms():

    # get group details
	r = requests.get(url+"/groups")

    # change JSON to dict for reading
	groups = r.json()

    # render rooms.html and pass header and room info to page
	return render_template("./rooms.html", header=headerinfo, dict=groups)


