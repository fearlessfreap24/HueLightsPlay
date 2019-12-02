import requests
import os
import time
from dotenv import load_dotenv

# read .env file to get Hue Key
load_dotenv()

# read HUEKEY environmental variable
hk = os.getenv("HUEKEY")
print(hk)
# create base url
url = "http://192.168.0.108/api/"+hk

# getting lights data
r = requests.get(url+"/lights")

# turn lights JSON into a dict for reading
dict = r.json()

# print name and light state for each light.
for i in dict:
    print("{}, {}, on: {}".format(i, dict[i]['name'], dict[i]['state']['on']))

# this will be a sequence
# Dylan Office - 5, Hall Left - 6, and LR leopard - 3
onoff = True
requests.put(url+"/lights/5/state", json={'on': onoff, 'bri': 1})
requests.put(url+"/lights/6/state", json={'on': onoff, 'bri': 1})
requests.put(url+"/lights/3/state", json={'on': onoff, 'bri': 1})
print('sleep 45')
time.sleep(45)
print('end sleep 45')
requests.put(url+"/lights/5/state", json={'on': False})
print('dylan off')
time.sleep(15)
print('end sleep 15')
requests.put(url+"/lights/6/state", json={'on': False})
print('hall off')
time.sleep(20)
print('end sleep 20')
requests.put(url+"/lights/3/state", json={'on': False})
print('leopard off')

