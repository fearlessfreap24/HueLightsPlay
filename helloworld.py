import requests
from flask import Flask,redirect,render_template, flash
from config import Config
from roomform import RoomForm

app = Flask(__name__)
app.config.from_object(Config)

# read HUEKEY environmental variable
hk = app.config["HUEKEY"]
hip = app.config["HUEIP"]


# routine to create base url
def url():
	return str("http://" + hip + "/api/" + hk)


# a dict to pass info for nav bar to jinja
def headerinfo():
	return {'Home': "/", 'Lights': "/lights", 'Special Functions': "/special", 'Rooms': "/rooms"}


# method to retrieve room names
def getrooms():
	# http request for rooms
	r = requests.get(url()+"/groups")
	# turn lights JSON into a dict for reading
	dicto = r.json()
	return dicto


# home page
@app.route('/')
def index():
	return render_template("index.html", header=headerinfo())


# test page
@app.route('/hello/')
def hello():
	return 'Hello World'


# display lights and light status
@app.route('/lights')
def lights():

	# getting lights data
    r = requests.get(url()+"/lights")

    # turn lights JSON into a dict for reading
    dicto = r.json()

    # render the template and pass dict to template
    return render_template('lights.html', dict=dicto, header=headerinfo())


# function for dylan light on/off
@app.route('/dylan')
def dylan():
    # request info for light 5
	light5 = requests.get(url()+"/lights/5/")

	# create dict for reading
	control5 = light5.json()

	# remember the current state of the light
	currStatus = control5['state']['on']

	# change light state to the opposite of the current state
	requests.put(url()+"/lights/5/state", json={'on': not currStatus})

	# return to the lights.html page
	return redirect("./lights")


# function to turn off leopard lamp and dylan light
@app.route('/leopard')
def leopard():

	# change light state to off
	requests.put(url()+"/lights/5/state", json={'on': False })
	requests.put(url()+"/lights/3/state", json={'on': False })

	# return to the lights.html page
	return redirect("./lights")


# a page for links to leopard() and dylan()
@app.route('/special')
def special():

    # render special.html and pass header info
    return render_template("./special.html", header=headerinfo())


# a page to display rooms and rooms stauts
@app.route('/rooms')
def rooms():
    groups = getrooms()

    # render rooms.html and pass header and room info to page
    return render_template("./rooms.html", header=headerinfo(), dict=groups)


# morning on routine
@app.route('/morning')
def morning():

	# turn on bedroom lights at full brightness
	requests.put(url() + "/groups/2/action", json={'on': True, 'bri': 254})

	# turn on living room light at full brightness
	requests.put(url() + "/groups/1/action", json={'on': True, 'bri': 254})

	# turn on hall lights at half brightness
	requests.put(url() + "/groups/5/action", json={'on': True, 'bri': 127})

	# send back to lights page
	return redirect("./lights")


# routine for darken ship
@app.route('/dogzebra')
def dogzebra():
	groups = getrooms()

	# living room = 1
	# master bedroom = 2
	# paige's office = 3
	# dylan's office = 4
	# hallway = 5
	requests.put(url() + "/groups/1/action", json={'on': False})
	requests.put(url() + "/groups/2/action", json={'on': False})
	requests.put(url() + "/groups/3/action", json={'on': False})
	requests.put(url() + "/groups/4/action", json={'on': False})
	requests.put(url() + "/groups/5/action", json={'on': False})

	# send back to lights page
	return redirect("./lights")


@app.route('/roomform', methods=['GET', 'POST'])
def roomform():
	groups = getrooms()
	form = RoomForm()
	form.room.choices = [(int(room), groups[room]['name']) for room in groups]
	print(f"{form.validate_on_submit()}")
	if form.validate_on_submit():
		room = form.room.data
		intensity = form.intensity.data
		onoff = form.onoff.data

		print(f'{room} {intensity} {onoff}')

		requests.put(url() + f"/groups/{room}/action", json={'on': onoff, 'bri': int(intensity)})

		return redirect("./rooms")
	else:
		# groups = getrooms()
		# form.room.choices = [(room, groups[room]['name']) for room in groups]
		flash(form.errors)
		return render_template('./roomform.html', header=headerinfo(), form=form)
