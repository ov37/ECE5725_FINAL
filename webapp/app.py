from flask import Flask, request, render_template
import paho.mqtt.publish as publish
import json
import time
import requests

MQTT_API_KEY = 'SESPS20JB3HS9FNO'
WRITE_API_KEY = '1TIH3KFRFKEWYA8L'
channelID = "1040309"
field_number = '2'


topic = "channels/" + channelID + "/publish/fields/field" + field_number + "/" + WRITE_API_KEY

app = Flask(__name__)

msg_dict = {}

def sendMessage(message):
    print(message)
    payload = message
    r = publish.single(topic, payload, hostname = "mqtt.thingspeak.com", port = 1883, auth = {'username':"user", 'password':MQTT_API_KEY})
    time.sleep(2)
    r = requests.get('https://api.thingspeak.com/channels/1040309/feeds.json?api_key=2D4RRJVU70QBL1YS&results=1')
    while( str(r.json()["feeds"][0]["field" + field_number]) !=  str(message) ):
        print(r.json()["feeds"][0]["field" + field_number] )
        print "Retrying..."
        r = publish.single(topic, payload, hostname = "mqtt.thingspeak.com", port = 1883, auth = {'username':"user", 'password':MQTT_API_KEY})
        time.sleep(2)
        r = requests.get('https://api.thingspeak.com/channels/1040309/feeds.json?api_key=2D4RRJVU70QBL1YS&results=1')
        #print(r.json()["feeds"][0]["field" + field_number])


@app.route('/', methods=['POST', 'GET'])
def message_form_post():
    if request.method == 'GET':
        return render_template('temp.html')
    elif request.method =='POST':
        if request.form.get('Hey!') == 'Hey!':
            message = "Hey!"
        elif request.form.get('I miss you!') == 'I miss you!':
            message = "I miss you!"
        elif request.form.get('How are you?') == 'How are you?':
            message = "How are you?"
        elif request.form.get('Thinking of you') == 'Thinking of you':
            message = "Thinking of you"
        elif request.form.get('See you soon!') == 'See you soon!':
            message = "See you soon!"
        else:
            message = request.form['message']
        #print(message)
        #payload = message
        #r = publish.single(topic, payload, hostname = "mqtt.thingspeak.com", port = 1883, auth = {'username':"user", 'password':MQTT_API_KEY})
        #print(r)
        sendMessage(message)
    #msg_dict[message] = message

    #templateData = {
    #        'msg_dict' : msg_dict
    #}

    #send message to the other server here, maybe via FIFO?

    #return render_template('page.html', **templateData)
    return render_template('temp.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')


