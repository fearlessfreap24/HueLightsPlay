import requests as req
import os
from dotenv import load_dotenv
import datetime as dt
import json


# read .env file
load_dotenv()
hk = os.getenv('HUEKEY')
hip = os.getenv('HUEIP')
IPGEO = os.getenv("IPGEO")
MWSTARTTIME = dt.time(23, 0, 0)
MWENDTIME = dt.time(5, 0, 0)


def pp(toPrint):
    print()
    print(toPrint)
    print()


def jpp(toPrint):
    print()
    print(json.dumps(toPrint, indent=2))
    print()


# def isBigMaintWindow():
#     mwStart = dt.datetime.combine( dt.datetime.today(), MWSTARTTIME)
#     mwEnd = dt.datetime.combine(dt.datetime.today(), MWENDTIME)

#     # Eastern DST = -5
#     # Alaska/Hawaii = -11

#     easternDst = dt.timedelta(hours=5)
#     alaskaHawaii = dt.timedelta(hours=11)
#     utcMwStart = mwStart + easternDst
#     utcMwEnd = mwEnd + alaskaHawaii

#     utctime = dt.datetime.utcnow()

#     return utctime.hour >= utcMwStart.hour and utctime.hour < utcMwEnd.hour


# def isActualMaintWindow(lat, longi):
#     if not isBigMaintWindow():
#         return False

#     ipgeo = f"https://api.ipgeolocation.io/timezone?apiKey={IPGEO}&lat={lat}&long={longi}"
#     ipgeoInfo = req.get(ipgeo).json()
#     tzOffset = int(ipgeoInfo['timezone_offset'])
#     dst = int(ipgeoInfo['dst_savings'])

#     today = dt.datetime.today()
#     mwStart = dt.datetime.combine(today, MWSTARTTIME)
#     mwEnd = dt.datetime.combine(today, MWENDTIME)

#     currentUtcTime = dt.datetime.utcnow()
#     timeZone = dt.timedelta(hours=abs(tzOffset+dst))
#     currentTime = currentUtcTime - timeZone

#     return currentTime.hour == mwStart.hour or currentTime.hour < mwEnd.hour



if __name__ == "__main__":
    # # Fort Worth Lat/Long
    # lat = "32.75"
    # longi = "-97.3333333"

    # timezoneAddress = "http://worldtimeapi.org/api/timezone/America/Chicago"
    # timezoneResults = req.get(timezoneAddress).json()
    # timezoneDateTime = dt.datetime.fromisoformat(timezoneResults['datetime'])
    # timezoneInt = int(str(timezoneDateTime.tzinfo).split(':')[0][-3:])
    # sunRiseSetAddress = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={longi}&formatted=0"
    # sunriseSet = req.get(sunRiseSetAddress).json()
    # timezone = dt.timedelta(hours=abs(timezoneInt))
    # sunriseapi = sunriseSet['results']['sunrise']
    # sunsetapi = sunriseSet['results']['sunset']
    # sunrise = dt.datetime.fromisoformat(sunriseapi)-timezone
    # sunset = dt.datetime.fromisoformat(sunsetapi)-timezone

    # print(f"\nsunrise = {str(sunrise.date())} {str(sunrise.time())}")
    # print(f"sunset = {str(sunset.date())} {str(sunset.time())}\n")

    # print(f"Fort Worth in maintenance window? {isActualMaintWindow(lat, longi)}")

    # bbb [0..127] – is a bit mask to indicate which days in a 7 day cycle are chosen.
    # •  so bbb = 0MTWTFSS – So only Tuesdays is 00100000 = 32
    # •	Weekdays is 01111100 = 124

    # newSunSetTime = {'localtime': f"W127/T{str(sunset.time())}A00:10:00"}
    # # changeOutsideLightOnTime = req.put(f"http://{HUEIP}/api/{HUEKEY}/schedules/2", json=newSunSetTime).json()
    # print()
    # print(newSunSetTime)

    # ssSrDiff = sunrise - sunset
    # print(f"\nthe difference is {str(ssSrDiff).split(',')[1]}")
    hueaddress = f"http://{hip}/api/{hk}/"
    # pp(hueaddress)
    rules = req.get(hueaddress + "rules/2").json()
    jpp(rules)
#     update_rule_2 = {
#                     "actions": [
#                         {
#                             "address": "/groups/6/action",
#                             "method": "PUT",
#                             "body": {
#                                 "on": True
#                             }
#                         },
#                             {
#                             "address": "/groups/7/action",
#                             "method": "PUT",
#                             "body": {
#                                 "on": True
#                             }
#                         },
#                             {
#                             "address": "/groups/5/action",
#                             "method": "PUT",
#                             "body": {
#                                 "on": True
#                             }
#                         }
#                     ]
#                 }

# send_update = req.put(hueaddress + "rules/2", json=update_rule_2).json()
# jpp(send_update)