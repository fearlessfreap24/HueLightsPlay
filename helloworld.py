import requests
from flask import Flask, redirect, render_template, flash, request
from config import Config
import HueAdmin as HA
import datetime as dt
import json
from players import jj_players


app = Flask(__name__)
app.config.from_object(Config)

BAD_INPUT = {'badInput': True}


# a dict to pass info for nav bar to jinja
def headerinfo():
    return {'Home': "/", 'Lights': "/lights", 'Special Functions': "/special", 'Rooms': "/rooms"}


def getTimeZone():
    # get timezone and whittle it down to an integer
    timezoneAddress = "http://worldtimeapi.org/api/timezone/America/Chicago"
    # timezoneAddress = "http://worldtimeapi.org/api/timezone/America/Chicago"
    timezoneCall = requests.get(timezoneAddress)
    goodTimeZone = timezoneCall.status_code == 200
    if goodTimeZone:
        timezoneResults = timezoneCall.json()
        timezoneDateTime = dt.datetime.fromisoformat(timezoneResults['datetime'])
        timezoneInt = int(str(timezoneDateTime.tzinfo).split(':')[0][-3:])

        return { 'isSuccess': goodTimeZone, 'tz': timezoneInt }
    else:
        return { 'isSuccess': goodTimeZone }


def getSunRiseSet():
    
    # Fort Worth Lat/Long
    lat = "32.75"
    longi = "-97.3333333"
    timezone = getTimeZone()
    if timezone['isSuccess']:
        timezoneInt = timezone['tz']
    # get sunrise/sunset info and apply timezone
    sunRiseSetAddress = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={longi}&formatted=0"
    # sunRiseSetAddress = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={longi}&formatted=0"
    sunriseSetCall = requests.get(sunRiseSetAddress, verify=False)
    goodApiCall = sunriseSetCall.status_code == 200
    sunriseSet = sunriseSetCall.json()
    if goodApiCall and timezone['isSuccess']:
        timezone = dt.timedelta(hours=abs(timezoneInt))
        sunriseapi = sunriseSet['results']['sunrise']
        sunsetapi = sunriseSet['results']['sunset']
        sunrise = dt.datetime.fromisoformat(sunriseapi)-timezone
        sunset = dt.datetime.fromisoformat(sunsetapi)-timezone
        return { 'isSuccess': goodApiCall, "sunrise": sunrise, "sunset": sunset }
    else:
        return {'isSuccess': goodApiCall and timezone['isSuccess'] }


def updateSunsetTime():
    
    ssTimes = getSunRiseSet()
    if ssTimes['isSuccess']:
        sunset = ssTimes["sunset"]
        sunrise = ssTimes["sunrise"]
        # apply new sunset time to schedule
        newSunSetTime = {'localtime': f"W127/T{str(sunset.time())}A00:10:00"}
        newSunRiseTime = {'localtime': f"W127/T{str(sunrise.time())}A00:10:00"}
        changeOutsideLightOnTime = HA.update_schedule(2, newSunSetTime)
        changeOutsideLightOffTime = HA.update_schedule(4, newSunRiseTime)
        print(changeOutsideLightOnTime)
        print(changeOutsideLightOffTime)
    else:
        print("There was an error getting sunrise/sunset times")


# home page
@app.route('/')
def index():
    return render_template("index.html", header=headerinfo(), active="Home")


# # test page
# @app.route('/hello/')
# def hello():
#     return 'Hello World'


# display lights and light status
@app.route('/lights')
def lights():
    # get lights information
    dicto = HA.get_lights()

    # render the template and pass dict to template
    return render_template('lights.html', dict=dicto, header=headerinfo(), active="Lights")


# function for dylan light on/off
@app.route('/dylan')
def dylan():
    # request info for group 4
    group4 = HA.get_groups(4)

    # remember the current state of the light
    currStatus = group4['action']['on']

    # change light state to the opposite of the current state
    change_state = HA.change_group_state(4, {'on': not currStatus})

    if change_state:
        return redirect("./lights")
    return special()


# function to turn off leopard lamp and dylan light
@app.route('/leopard')
def leopard():
    # change light state to off
    HA.change_group_state(4, {'on': False})
    HA.change_light_state(3, {'on': False})

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
    groups = HA.get_groups()

    # render rooms.html and pass header and room info to page
    return render_template("./rooms.html", header=headerinfo(), dict=groups, active="Rooms")


# morning on routine
@app.route('/morning')
def morning():
    # turn on bedroom lights at full brightness
    HA.change_group_state(2, {'on': True, 'bri': 254})

    # turn on living room light at full brightness
    HA.change_group_state(1, {'on': True, 'bri': 254})

    # turn on hall lights at half brightness
    HA.change_group_state(5, {'on': True, 'bri': 127})

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
    HA.change_group_state(1, {'on': False})
    HA.change_group_state(3, {'on': False})
    HA.change_group_state(2, {'on': False})
    HA.change_group_state(4, {'on': False})
    HA.change_group_state(5, {'on': False})

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
    HA.change_light_state(12, {'bri': 50})
    HA.change_light_state(1, {'on': False})
    HA.change_group_state(1, {'on': False})
    HA.change_group_state(3, {'on': False})
    HA.change_group_state(4, {'on': False})
    HA.change_group_state(5, {'on': False})

    # send back to lights page
    return redirect("./lights")


@app.route('/api/lightstatus', methods=['GET'])
def lightstatus():

    light = request.args.get('light')
    if not light.isdigit():
        return BAD_INPUT

    return HA.get_lights(light)


@app.route('/api/lightonoff', methods=['GET', 'POST'])
def lightonoff():

    light = request.args.get('light')

    onoff = request.args.get('onoff').lower()

    if not light.isdigit():
        return BAD_INPUT

    if onoff == 'on':
        onoff = True
    elif onoff == 'off':
        onoff = False
    else:
        return BAD_INPUT

    HA.change_light_state(light, {'on': onoff})

    return HA.get_lights(light)


@app.route('/api/roomstatus', methods=['GET'])
def roomstatus():
    
    room = request.args.get('room')
    if not room.isdigit():
        return BAD_INPUT

    return HA.get_groups(room)


@app.route('/api/roomonoff', methods=['GET'])
def roomonoff():

    room = request.args.get('room')

    if not room.isdigit():
        return BAD_INPUT

    onoff = request.args.get('onoff').lower()

    if onoff == 'on':
        onoff = True
    elif onoff == "off":
        onoff = False
    else:
        return BAD_INPUT

    HA.change_group_state(room, {'on': onoff})

    return HA.get_groups(room)


@app.route('/api/roomintens', methods=['GET'])
def roomintens():

    room = request.args.get('room')

    if not room.isdigit():
        return BAD_INPUT

    intens = request.args.get('intens')

    if not intens.isdigit():
        return BAD_INPUT
    elif not 1 <= int(intens) <= 254:
        return BAD_INPUT

    HA.change_group_state(room, {'bri': int(intens)})

    return HA.get_groups(room)


@app.route('/api/lightintens', methods=['GET'])
def lightintens():

    light = request.args.get('light')
    if not light.isdigit():
        return BAD_INPUT

    intens = request.args.get('intens')
    if not intens.isdigit():
        return BAD_INPUT
    elif not 1 <= int(intens) <= 254:
        return BAD_INPUT

    HA.change_light_state(light, {'bri': int(intens)})

    return HA.get_lights(light)


@app.route('/api/sunrisesunset', methods=['GET'])
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
    if ssTimes['isSuccess']:
        returnDict["sunrise"] = ssTimes["sunrise"]
        returnDict["sunset"] = ssTimes["sunset"]
    else:
        returnDict["sunrise"] = "Unable to get time"
        returnDict["sunset"] = "Unable to get time"
    # "Turn On Outside"
    # "Turn Off Outside"
    schedules = HA.get_schedules()
    for i in schedules:
        if schedules[i]["name"] == "Turn On Outside":
            returnDict["outsideOn"] = schedules[i]["localtime"]
        elif schedules[i]["name"] == "Turn Off Outside":
            returnDict["outsideOff"] = schedules[i]["localtime"]

    sensor7 = HA.get_sensors(7)
    returnDict["sensorStatus"] = str(sensor7["state"]["flag"])
    timezoneInt = getTimeZone()
    if timezoneInt['isSuccess']:
        timezone = dt.timedelta(hours=abs(timezoneInt['tz']))
    else:
        timezone = dt.timedelta(hours=6)
    sensorDateTime = dt.datetime.fromisoformat(sensor7["state"]["lastupdated"])
    sensorDateTimeWithTz = sensorDateTime-timezone
    returnDict["sensorLastUpdate"] = sensorDateTimeWithTz

    return returnDict


@app.route('/OutsideStatus')
def outsideStatus():
    info = ssStatus()
    return render_template("./outsidestatus.html", header=headerinfo(), dict=info)


@app.route('/jj')
def bush_rotation():
    jjp = jj_players()
    one_day = 86400
    today = int((dt.datetime.now().timestamp()/one_day)%15)
    tomm = today+1
    two_day = today+2
    spear_grass = jjp.get_spear_grass()
    birthday_bush = jjp.check_bday()
    purple_smokebush = jjp.purple_smokebush['ign']
    marmalade_bush = jjp.marmalade_bush['ign']
    if birthday_bush:
        butterfy_bush = birthday_bush['ign']
    else:
        butterfy_bush = ""
    return f"""<p>
    {f'<p><h2>Butterfly Bush</h2></p><p>{butterfy_bush}</p>' if birthday_bush else ''}
    <p><h2>Purple Smokebush</h2></p><p>{purple_smokebush}</p>
    <p><h2>Marmalade Bush</h2></p><p>{marmalade_bush}</p>
    <p><h2>Spear Bushes</h2></p><p>{', '.join(spear_grass)}</p>
    </p>"""


if __name__ == "__main__":
    # Testing
    # app.run(debug=True)
    # Production
    app.run(host="0.0.0.0", port=5000)
    # print(ssStatus())
