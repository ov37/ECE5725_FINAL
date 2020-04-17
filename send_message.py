import requests

API_KEY = "1TIH3KFRFKEWYA8L"
x = "hello again"
payload = {'api_key':API_KEY, 'field1':str(x)}
print "X is " + x
r = requests.post('https://api.thingspeak.com/update', params=payload)
print r
