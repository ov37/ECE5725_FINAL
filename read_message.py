import requests
import json

r = requests.get('https://api.thingspeak.com/channels/1040309/feeds.json?api_key=2D4RRJVU70QBL1YS')
#&start=2020-04-17%2016:15:00&timezone=America%2FNew_York'
print(r.json())["feeds"]
print(r)
print(r.json())["feeds"][5]["field1"]
