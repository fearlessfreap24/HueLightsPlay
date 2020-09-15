import requests as req
from dotenv import load_dotenv
import os
import datetime as dt


load_dotenv()
hk = os.getenv("HUEKEY")
hip = os.getenv("HUEIP")
hueurl = f"http://{hip}/api/{hk}/"


def turnOnTestGroup():
    turnOnGroup8 = req.put(f"{hueurl}groups/8/action", json={ "on": True } ).json()
    print(turnOnGroup8)


def bumpSensor7():
    getSensorState = req.get(f"{hueurl}sensors/7/").json()
    newState = not getSensorState["state"]["flag"]
    changeSensor7 = req.put(f"{hueurl}sensors/7/state", json={ "flag": newState}).json()
    print(changeSensor7)


def updateSunsetTime():
    ssTimes = getSunRiseSet()
    sunset = ssTimes["sunset"]
    sunrise = ssTimes["sunrise"]
    # apply new sunset time to schedule
    newSunSetTime = {'localtime': f"W127/T{str(sunset.time())}A00:10:00"}
    newSunRiseTime = {'localtime': f"W127/T{str(sunrise.time())}A00:10:00"}
    # changeOutsideLightOnTime = req.put(f"http://{hip}/api/{hk}/schedules/2", json=newSunSetTime).json()
    # changeOutsideLightOffTime = req.put(f"http://{hip}/api/{hk}/schedules/4", json=newSunRiseTime).json()
    # print(changeOutsideLightOnTime)
    # print(changeOutsideLightOffTime)
    print(newSunSetTime)
    print(newSunRiseTime)


def getSunRiseSet():
    # Fort Worth Lat/Long
    lat = "32.75"
    longi = "-97.3333333"
    # get timezone and whittle it down to an integer
    timezoneAddress = "http://worldtimeapi.org/api/timezone/America/Chicago"
    timezoneResults = req.get(timezoneAddress).json()
    timezoneDateTime = dt.datetime.fromisoformat(timezoneResults['datetime'])
    timezoneInt = int(str(timezoneDateTime.tzinfo).split(':')[0][-3:])
    # get sunrise/sunset info and apply timezone
    sunRiseSetAddress = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={longi}&formatted=0"
    sunriseSet = req.get(sunRiseSetAddress).json()
    timezone = dt.timedelta(hours=abs(timezoneInt))
    sunriseapi = sunriseSet['results']['sunrise']
    sunsetapi = sunriseSet['results']['sunset']
    sunrise = dt.datetime.fromisoformat(sunriseapi)-timezone
    sunset = dt.datetime.fromisoformat(sunsetapi)-timezone

    return { "sunrise": sunrise, "sunset": sunset }


# lights for testing - 5, 7, 13


# this created group 8
# newGroup = {
#             "lights": ["5", "7", "13"],
#             "name": "TestGroup",
#             "type": "LightGroup"
# }

# createGroup = req.post(f"{hueurl}groups", json=newGroup).json()

# print(createGroup)


# # created schedule 5
# newSchedule = {
#     "name": "Turn Off Outside",
#     "command":
#         {
#             "address": f"/api/{hk}/sensors/7/state",
#             "method": "PUT",
#             "body":
#             {
#                 "flag": False
#             },
#         },
#     "localtime": "W127/T07:11:00"
# }

# createSchedule = req.post(f"{hueurl}schedules", json=newSchedule).json()
# print(createSchedule)
# print(req.get(f"{hueurl}schedules/4").json())

# 0MTWtFSS
# 00000111

# created schedule 4
# newSchedule = {
#                 "name": "Turn Off TestGroup",
#                 "command": {
#                     "address": f"api/{hk}/groups/8/action",
#                     "method": "PUT",
#                     "body": {
#                         "on": False
#                     }
#                 },
#                 "localtime": "W007/T11:45:00"
# }
# createSchedule = req.post(f"{hueurl}schedules", json=newSchedule).json()
# print(createSchedule)

# changeOnTime = { "localtime": "W127/T15:46:00" }
# updateOnTime = req.put(f"{hueurl}schedules/2", json=changeOnTime).json()
# changeOffTime = { "localtime": "W127/T15:38:00" }
# updateOffTime = req.put(f"{hueurl}schedules/4", json=changeOffTime).json()
# print(updateOnTime)
# print(updateOffTime)

# getGroupState = req.get(f"{hueurl}groups/8").json()


# created rule 2
# offRule = {
#     "name": "Turn On Test Group",
#     "conditions": [
#         {
#             "address": "/sensors/7/state/flag",
#             "operator": "dx"
#         },
#         {
#             "address": "/sensors/7/state/flag",
#             "operator": "eq",
#             "value": "false"
#         }
#     ],
#     "actions": [
#         {
#             "address": "/groups/6/action",
#             "method": "PUT",
#             "body": {
#                 "on": False
#             }
#         },
#         {
#             "address": "/groups/7/action",
#             "method": "PUT",
#             "body": {
#                 "on": False
#             }
#         }
#     ]
# }

# addNewRule = req.post(f"{hueurl}rules", json=offRule).json()
# print(addNewRule)


if __name__ == "__main__":
    # turnOnTestGroup()
    # bumpSensor7()
    # print(req.put(f"{hueurl}rules/3", json={ "name": "Turn Off Outside"}).json())
    # print(req.put(f"{hueurl}rules/2", json={ "name": "Turn On Outside"}).json())
    # updateSunsetTime()
    print("done")

