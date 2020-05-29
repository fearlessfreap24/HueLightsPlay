import requests
from flask import Flask, redirect, render_template, flash, request
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
    r = requests.get(url() + "/groups")
    # turn lights JSON into a dict for reading
    dicto = r.json()
    return dicto


def getlights():
    # getting lights data
    r = requests.get(url() + "/lights")
    # turn lights JSON into a dict for reading
    dicto = r.json()
    return dicto


# home page
@app.route('/')
def index():
    return render_template("index.html", header=headerinfo(), active="Home")


# test page
@app.route('/hello/')
def hello():
    return 'Hello World'


# display lights and light status
@app.route('/lights')
def lights():
    # get lights information
    dicto = getlights()

    # render the template and pass dict to template
    return render_template('lights.html', dict=dicto, header=headerinfo(), active="Lights")


# function for dylan light on/off
@app.route('/dylan')
def dylan():
    # request info for light 5
    light5 = requests.get(url() + "/lights/5/")

    # create dict for reading
    control5 = light5.json()

    # remember the current state of the light
    currStatus = control5['state']['on']

    # change light state to the opposite of the current state
    requests.put(url() + "/lights/5/state", json={'on': not currStatus})

    # return to the lights.html page
    return redirect("./lights")


# function to turn off leopard lamp and dylan light
@app.route('/leopard')
def leopard():
    # change light state to off
    requests.put(url() + "/lights/5/state", json={'on': False})
    requests.put(url() + "/lights/3/state", json={'on': False})

    # return to the lights.html page
    return redirect("./lights")


# a page for links to leopard() and dylan()
@app.route('/special')
def special():
    # render special.html and pass header info
    return render_template("./special.html", header=headerinfo(), active="Special Functions")


# a page to display rooms and rooms stauts
@app.route('/rooms')
def rooms():
    # get room information
    groups = getrooms()

    # render rooms.html and pass header and room info to page
    return render_template("./rooms.html", header=headerinfo(), dict=groups, active="Rooms")


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
    # get dict of rooms
    groups = getrooms()
    # instantiate form
    form = RoomForm()
    # add choices to SelectField using rooms
    form.room.choices = [(int(room), groups[room]['name']) for room in groups]
    # check to see if form validated
    if form.validate_on_submit():
        # extract data from submitted form
        room = form.room.data
        intensity = form.intensity.data
        onoff = form.onoff.data

        # send data to Hue to change room setting per form
        requests.put(url() + f"/groups/{room}/action", json={'on': onoff, 'bri': int(intensity)})
        # redirect to rooms.html to see changes
        return redirect("./rooms")
    # if validation failed or new form
    else:
        # get errors from submitted form
        flash(form.errors)
        # display roomform.html
        return render_template('./roomform.html', header=headerinfo(), form=form)


@app.route('/api/v1/resources/lightstatus', methods=['GET'])
def lightstatus():

    light = request.args.get('light')

    return requests.get(url() + f'/lights/{light}').json()


@app.route('/api/v1/resources/lightonoff', methods=['GET', 'POST'])
def lightonoff():

    light = request.args.get('light')

    onoff = request.args.get('onoff')

    if request.args.get('onoff') == 'on':
        onoff = True
    elif request.args.get('onoff') == 'off':
        onoff = False

    requests.put(url() + f"/lights/{light}/state", json={'on': onoff})

    return requests.get(url() + f"/lights/{light}").json()


@app.route('/api/v1/resources/roomstatus', methods=['GET'])
def roomstatus():

    room = request.args.get('room')

    return requests.get(url() + f"/groups/{room}").json()


@app.route('/api/v1/resources/roomonoff', methods=['GET'])
def roomonoff():

    room = request.args.get('room')

    onoff = request.args.get('onoff')

    if request.args.get('onoff') == 'on':
        onoff = True
    elif request.args.get('onoff') == "off":
        onoff = False

    requests.put(url() + f"/groups/{room}/action", json={'on': onoff})

    return requests.get(url() + f"/groups/{room}").json()


@app.route('/api/v1/resources/roomintens', methods=['GET'])
def roomintens():

    room = request.args.get('room')

    intens = request.args.get('intens')

    requests.put(url() + f"/groups/{room}/action", json={'bri': intens})

    return requests.get(url() + f"groups/{room}").json()
