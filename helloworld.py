import requests
from flask import Flask, redirect, render_template, flash, request
from config import Config
from roomform import RoomForm
import datetime as dt

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


def getTimeZone():
    # get timezone and whittle it down to an integer
    timezoneAddress = "http://worldtimeapi.org/api/timezone/America/Chicago"
    timezoneResults = requests.get(timezoneAddress).json()
    timezoneDateTime = dt.datetime.fromisoformat(timezoneResults['datetime'])
    timezoneInt = int(str(timezoneDateTime.tzinfo).split(':')[0][-3:])

    return timezoneInt


def getSunRiseSet():
    
    # Fort Worth Lat/Long
    lat = "32.75"
    longi = "-97.3333333"
    timezoneInt = getTimeZone()
    # get sunrise/sunset info and apply timezone
    sunRiseSetAddress = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={longi}&formatted=0"
    sunriseSet = requests.get(sunRiseSetAddress).json()
    timezone = dt.timedelta(hours=abs(timezoneInt))
    sunriseapi = sunriseSet['results']['sunrise']
    sunsetapi = sunriseSet['results']['sunset']
    sunrise = dt.datetime.fromisoformat(sunriseapi)-timezone
    sunset = dt.datetime.fromisoformat(sunsetapi)-timezone

    return { "sunrise": sunrise, "sunset": sunset }


def updateSunsetTime():
    
    ssTimes = getSunRiseSet()
    sunset = ssTimes["sunset"]
    sunrise = ssTimes["sunrise"]
    # apply new sunset time to schedule
    newSunSetTime = {'localtime': f"W127/T{str(sunset.time())}A00:10:00"}
    newSunRiseTime = {'localtime': f"W127/T{str(sunrise.time())}A00:10:00"}
    changeOutsideLightOnTime = requests.put(f"http://{hip}/api/{hk}/schedules/2", json=newSunSetTime).json()
    changeOutsideLightOffTime = requests.put(f"http://{hip}/api/{hk}/schedules/4", json=newSunRiseTime).json()
    print(changeOutsideLightOnTime)
    print(changeOutsideLightOffTime)


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
    
    updateSunsetTime()
    
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


@app.route('/prebed')
def prebed():
    # dylan's bed light = 1
    # paige's bed light = 12
    # paige's office = 3
    # dylan's office = 4
    # hallway = 5
    # # change light state
    requests.put(url() + "/lights/1/state", json={'bri': 50})
    requests.put(url() + "/lights/12/state", json={'on': False})
    requests.put(url() + "/groups/1/action", json={'on': False})
    requests.put(url() + "/groups/3/action", json={'on': False})
    requests.put(url() + "/groups/4/action", json={'on': False})
    requests.put(url() + "/groups/5/action", json={'on': False})

    # send back to lights page
    return redirect("./lights")


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

    requests.put(url() + f"/groups/{room}/action", json={'bri': int(intens)})

    return requests.get(url() + f"/groups/{room}").json()


@app.route('/api/v1/resources/lightintens', methods=['GET'])
def lightintens():

    light = request.args.get('light')

    intens = request.args.get('intens')

    requests.put(url() + f"/lights/{light}/state", json={'bri': int(intens)})

    return requests.get(url() + f"/lights/{light}").json()


@app.route('/api/v1/resources/sunrisesunset', methods=['GET'])
def ssStatus():
    returnDict = {
        "sunrise": "",
        "sunset": "",
        "outsideOn": "",
        "outsideOff": "",
        "sensorStatus": "",
        "sensorLastUpdate": ""
    }
    ssTimes = getSunRiseSet()
    returnDict["sunrise"] = ssTimes["sunrise"]
    returnDict["sunset"] = ssTimes["sunset"]
    # "Turn On Outside"
    # "Turn Off Outside"
    schedules = requests.get(f"{url()}/schedules").json()
    for i in schedules:
        if schedules[i]["name"] == "Turn On Outside":
            returnDict["outsideOn"] = schedules[i]["localtime"]
        elif schedules[i]["name"] == "Turn Off Outside":
            returnDict["outsideOff"] = schedules[i]["localtime"]

    sensor7 = requests.get(f"{url()}/sensors/7").json()
    returnDict["sensorStatus"] = str(sensor7["state"]["flag"])
    timezoneInt = getTimeZone()
    timezone = dt.timedelta(hours=abs(timezoneInt))
    sensorDateTime = dt.datetime.fromisoformat(sensor7["state"]["lastupdated"])
    sensorDateTimeWithTz = sensorDateTime-timezone
    returnDict["sensorLastUpdate"] = sensorDateTimeWithTz

    return returnDict


@app.route('/OutsideStatus')
def outsideStatus():
    info = ssStatus()
    return render_template("./outsidestatus.html", header=headerinfo(), dict=info)
