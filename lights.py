import requests
import os
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
    print("{}, on: {}".format(dict[i]['name'], dict[i]['state']['on']))

