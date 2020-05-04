#!/usr/bin/env python
#env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time

#import requests
import json
import paho.mqtt.client as mqtt

MQTT_API_KEY = 'SESPS20JB3HS9FNO'
READ_API_KEY = '2D4RRJVU70QBL1YS'

field_number = '1'
new_messages = 0
messages = [""]
first = 1
my_text = ""

def init_client(client):
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("user", MQTT_API_KEY)
    client.connect("mqtt.thingspeak.com", 1883, 60)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('channels/1040309/subscribe/fields/field' + field_number + '/' + READ_API_KEY)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    print 1
    messages[new_messages] = str(msg.payload)
    #new_messages += 1 
    #my_text = "Got" #str(msg.payload)

def prepare_canvas(offscreen_canvas, my_text):
    graphics.DrawText(offscreen_canvas, font, 0, 10, textColor, my_text)
    return offscreen_canvas

def display(offscreen_canvas, matrix):
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

def scroll_prep(offscreen_canvas, message): 
    offscreen_canvas.Clear()
    len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, message)
    pos -= 1
    if (pos + len < 0):
        pos = offscreen_canvas.width



# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'

matrix = RGBMatrix(options = options)
offscreen_canvas = matrix.CreateFrameCanvas()
font = graphics.Font()
font.LoadFont("../../../fonts/6x10.bdf")
textColor = graphics.Color(204, 102, 255)
pos = offscreen_canvas.width

client = mqtt.Client()
init_client(client)

try:
    client.loop_start()
    #display(offscreen_canvas, matrix)
    while True:
        #time.sleep(0.05)
        #if(new_messages > 0):
        #    my_text = messages[i]
            #display(offscreen_canvas, matrix)
        #    new_messages -= 1
        #    time.sleep(5)
        #    i += 1
        #else:
        #    i = 0

        #    start = time.time()
        #if((time.time() - start) > 10):
        #        i += 1
        #        new_messages -= 1
        
        #else:
        #    my_text = "None"

        print messages[0]

        #offscreen_canvas.Clear()
        #prepare_canvas(offscreen_canvas, messages[0])
        #display(offscreen_canvas, matrix)
        #time.sleep(1)
        
        scroll_prep(offscreen_canvas, matrix, message[0])
        time.sleep(0.05)
        display(offscreen_canvas, matrix)

except KeyboardInterrupt():
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
