import requests
import json
import paho.mqtt.client as mqtt

MQTT_API_KEY = 'SESPS20JB3HS9FNO'
READ_API_KEY = '2D4RRJVU70QBL1YS'

field_number = '1'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('channels/1040309/subscribe/fields/field' + field_number + '/' + READ_API_KEY)
    #client.subscribe('channels/1040309/subscribe/json/' + READ_API_KEY)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("user", MQTT_API_KEY)

client.connect("mqtt.thingspeak.com", 1883, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    client.disconnect()
