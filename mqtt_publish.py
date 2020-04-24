import paho.mqtt.publish as publish
import json

MQTT_API_KEY = 'SESPS20JB3HS9FNO'
WRITE_API_KEY = '1TIH3KFRFKEWYA8L'
channelID = "1040309"
field_number = '1'


topic = "channels/" + channelID + "/publish/fields/field" + field_number + "/" + WRITE_API_KEY
#topic = "channels/" + channelID + "/publish/" + WRITE_API_KEY

#client.username_pw_set("user", MQTT_API_KEY)

#client.connect("mqtt.thingspeak.com", 1883, 60)
x = raw_input("Send message: ")
payload = str(x)
print "X is: " + payload
r = publish.single(topic, payload, hostname = "mqtt.thingspeak.com", port = 1883, auth = {'username':"user", 'password':MQTT_API_KEY})
print r
