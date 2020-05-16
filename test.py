#!/usr/bin/env python
#env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time
from PIL import Image
#import requests
import json
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)
present = 0


MQTT_API_KEY = 'SESPS20JB3HS9FNO'
READ_API_KEY = '2D4RRJVU70QBL1YS'

field_number = '1'
new_messages = 0
messages = [""]
first = 1
my_text = ""
pos = 0

heart = Image.open("heart.png").resize((15,15))
smiley = Image.open("smiley.png").resize((15,15))

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
    #messages[new_messages] = str(msg.payload)
    messages.append(str(msg.payload))
    #new_messages += 1 
    #my_text = "Got" #str(msg.payload)

def prepare_canvas(offscreen_canvas, my_text):
    graphics.DrawText(offscreen_canvas, font, 0, 10, textColor, my_text)
    return offscreen_canvas

def display(offscreen_canvas, matrix):
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

def scroll_prep(offscreen_canvas, message, pos): 
    offscreen_canvas.Clear()
    length = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, message)
    pos -= 1
    if (pos + length < 0):
        pos = offscreen_canvas.width


def parseText(oddscreen_canvas, message):
    if "<heart>" in message:
        offscreen_canvas.SetImage(heart.convert('RGB'), 10, 15)
        message = message[:message.find('<heart>')]
    elif "<smiley>" in message:
        offscreen_canvas.SetImage(smiley.convert('RGB'), 10, 15)
        message = message[:message.find('<smiley>')]

    return offscreen_canvas, message


# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'

matrix = RGBMatrix(options = options)
offscreen_canvas = matrix.CreateFrameCanvas()
font = graphics.Font()
font.LoadFont("../../../fonts/7x13.bdf")
textColor = graphics.Color(204, 102, 255)
pos = offscreen_canvas.width
#image = Image.open("heart.png")

client = mqtt.Client()
init_client(client)

message_num = 2

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

        #print messages[0]

        #offscreen_canvas.Clear()
        #prepare_canvas(offscreen_canvas, messages[0])
        #display(offscreen_canvas, matrix)
        #time.sleep(1)
        
        #scroll_prep(offscreen_canvas, messages[0], pos)
        x = GPIO.input(6)
        if (x==0):
            print("object detected")
            present = 1
        
        if (present==1) and (len(messages)>2) and (message_num<len(messages)):
            offscreen_canvas.Clear()
            offscreen_canvas, message = parseText(offscreen_canvas, messages[message_num])

            length = graphics.DrawText(offscreen_canvas, font, pos, 11, textColor, message)
            pos -= 1
            if (pos + length < 0):
                pos = offscreen_canvas.width
                if (message_num + 1 >= len(messages)):
                        present = 0
                        offscreen_canvas.Clear()
                message_num += 1
            display(offscreen_canvas, matrix)
 
        # can also use thumbnail() method
        #image = image.resize((15, 15))#, Image.ANTIALIAS)

        #offscreen_canvas.SetImage(image.convert('RGB'), 10, 15)
        #offscreen_canvas = parseText(offscreen_canvas, messages[0])
        time.sleep(0.05)
        #display(offscreen_canvas, matrix)

except KeyboardInterrupt():
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
