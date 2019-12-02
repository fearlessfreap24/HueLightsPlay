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
startbri = dict['5']['state']['bri']
dylanlighturl = "http://192.168.0.108/api/"+hk+"/lights/5/state"

# 15 seconds on lowest
# requests.put(dylanlighturl, json={'on': True, 'bri': 1})
# time.sleep(15)
# requests.put(dylanlighturl, json={'on': True, 'bri': startbri})

while True:
	print("Type a 'Q' in the first question to exit.")
	waittime = input("How many seconds to wait? (Whole numbers only): ")
	if waittime == "Q":
		break
	howbri = input("What is the brightness you would like? (1-255): ")

	requests.put(dylanlighturl, json={'on': True, 'bri': int(howbri)})
	time.sleep(int(waittime))
	requests.put(dylanlighturl, json={'on': True, 'bri': int(255)})

