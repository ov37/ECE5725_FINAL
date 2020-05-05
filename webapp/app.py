from flask import Flask, request, render_template
import paho.mqtt.publish as publish
import json

MQTT_API_KEY = 'SESPS20JB3HS9FNO'
WRITE_API_KEY = '1TIH3KFRFKEWYA8L'
channelID = "1040309"
field_number = '1'


topic = "channels/" + channelID + "/publish/fields/field" + field_number + "/" + WRITE_API_KEY

#while 1:
#    x = raw_input("Send message: ")
#    payload = str(x)
#    print "X is: " + payload
#    r = publish.single(topic, payload, hostname = "mqtt.thingspeak.com", port = 1883, auth = {'username':"user", 'password':MQTT_API_KEY})
 
app = Flask(__name__)

msg_dict = {}

@app.route('/', methods=['POST', 'GET'])
def message_form_post():
    if request.method == 'GET':
        return render_template('html_example.html')
    
    message = request.form['message']
    print(message)
    payload = message
    r = publish.single(topic, payload, hostname = "mqtt.thingspeak.com", port = 1883, auth = {'username':"user", 'password':MQTT_API_KEY})

    #msg_dict[message] = message

    #templateData = {
    #        'msg_dict' : msg_dict
    #}

    #send message to the other server here, maybe via FIFO?

    #return render_template('page.html', **templateData)
    return render_template('html_example.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')


