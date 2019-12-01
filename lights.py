import requests
import os
import time
from dotenv import load_dotenv

# read .env file to get Hue Key
load_dotenv()

# read HUEKEY environmental variable
hk = os.getenv("HUEKEY")

# create base url
url = "http://192.168.0.108/api/"+hk

# getting lights data
r = requests.get(url+"/lights")

# turn lights JSON into a dict for reading
dict = r.json()

# print name and light state for each light.
for i in dict:
    print("{}, {}, on: {}".format(i, dict[i]['name'], dict[i]['state']['on']))

# blinking light

# get my light info
dyllight = dict['5']

# get state into variable and create opposite state
onoff = dyllight['state']['on']
secondstate = not onoff

# make it flash 5 times with loop
# the json= part took a second to figure out
cnt = 0
while cnt != 5:
	requests.put(url+"/lights/5/state", json={'on': secondstate})
	time.sleep(2)
	requests.put(url+"/lights/5/state", json={'on': onoff})
	time.sleep(2)
	cnt += 1

