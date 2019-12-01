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

# this will be a sequence
# Dylan Office - 5, Hall Left - 6, and LR leopard - 3

requests.put(url+"/5/status" json={'bri':1, 'on': true})
requests.put(url+"/6/status" json={'bri':1, 'on': true})
requests.put(url+"/3/status" json={'bri':1, 'on': true})
time.sleep(60)

requests.put(url+"/5/status" json={'on': false})
time.sleep(15)
requests.put(url+"/6/status" json={'on': false})
time.sleep(30)
requests.put(url+"/3/status" json={'on': false})
