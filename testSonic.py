#!/usr/bin/env python
#env python
from samplebase import SampleBase
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time
from PIL import Image
import requests
import json
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import os
import sys
from datetime import datetime

# set up IR sensor GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)
present = 0

# Thingspeak API keys
MQTT_API_KEY = 'ENTER YOUR KEY'
READ_API_KEY = 'ENTER YOUR KEY'

field_number = '1'
new_messages = 0
messages = [""]
first = 1
my_text = ""
pos = 0

# open weather and message images and resize to fit
heart = Image.open("images/heart.png").resize((15,15))
smiley = Image.open("images/smiley.png").resize((15,15))
frowny = Image.open("images/frowny.png").resize((15,15))
flower = Image.open("images/flower.png").resize((15,15))
rain = Image.open("images/rain.png").resize((10,10))
cloud = Image.open("images/cloud.png").resize((10,10))
clear = Image.open("images/clear.png").resize((10,10))

# add correct weather image to canvas from api response string
def addWeather(offscreen_canvas, r):
    if(r == "Rain"):
        offscreen_canvas.SetImage(rain.convert('RGB'), 11, 20)
    elif(r == "Clear"):
        offscreen_canvas.SetImage(clear.convert('RGB'), 11, 20)
    elif(r == "Clouds"):
        offscreen_canvas.SetImage(cloud.convert('RGB'), 11, 20)
    return offscreen_canvas

# calculate and return next RGB value for smooth transition effect
def advanceColor(continuum):
    red = 0
    green = 0
    blue = 0

    if continuum <= 255:
        c = continuum
        blue = 255 - c
        red = c
    elif continuum > 255 and continuum <= 511:
        c = continuum - 256
        red = 255 - c
        green = c
    else:
        c = continuum - 512
        green = 255 - c
        blue = c

    return red, green, blue

# initalize MQTT client with Thingspeak
def init_client(client):
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("user", MQTT_API_KEY)
    client.connect("mqtt.thingspeak.com", 1883, 60)

# callback for connection with Thingspeak
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('channels/1040309/subscribe/fields/field' + field_number + '/' + READ_API_KEY)

# callback for new message from Thingspeak
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    messages.append(str(msg.payload))

# display canvas on matrix through double buffer
def display(offscreen_canvas, matrix):
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

# parse message for image indicator, place image on canvas, and remove indicator text from message
def parseText(offscreen_canvas, message):
    if "<heart>" in message:
        offscreen_canvas.SetImage(heart.convert('RGB'), 10, 15)
        message = message[:message.find('<heart>')]
    elif "<smiley>" in message:
        offscreen_canvas.SetImage(smiley.convert('RGB'), 10, 15)
        message = message[:message.find('<smiley>')]
    elif "<frowny>" in message:
        offscreen_canvas.SetImage(frowny.convert('RGB'), 10, 15)
        message = message[:message.find('<frowny>')]
    elif "<flower>" in message:
        offscreen_canvas.SetImage(flower.convert('RGB'), 10, 15)
        message = message[:message.find('<flower>')]
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

# start MQTT client
client = mqtt.Client()
init_client(client)

# initalize variables and get local Ithaca weather
message_num = 2
font_time = graphics.Font()
font_time.LoadFont("../../../fonts/6x10.bdf")
continuum = 0
r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Ithaca,newyork&APPID=96b3bf9496927da84dec45410b24f72d')
r = r.json()["weather"][0]["main"]

try:
    client.loop_start()
    while True:
        
        #if there are unread messages, check FIFO if user is present
        if (present==0):
            fifo = open("/home/pi/SONAR_FIFO.fifo", "r")
            for line in fifo:
                print(line)
                if line=="1":
                    x = 0
                    print("present")
                else:
                    x=1
            fifo.close()
        if ((x==0) and (present==0)):
            present=1
                
        # if user is present and there are unread messages
        if (present==1) and (len(messages)>2) and (message_num<len(messages)):
            offscreen_canvas.Clear()
            offscreen_canvas, message = parseText(offscreen_canvas, messages[message_num])

            length = graphics.DrawText(offscreen_canvas, font, pos, 11, textColor, message)
            pos -= 1
            # scroll text
            if (pos + length < 0):
                pos = offscreen_canvas.width
                if (message_num + 1 >= len(messages)):
                        present = 0
                        offscreen_canvas.Clear()
                message_num += 1
            display(offscreen_canvas, matrix)
        else:
            offscreen_canvas.Clear()
            
            # write current time to canvas
            graphics.DrawText(offscreen_canvas, font_time, 1, 18, textColor, datetime.now().strftime("%H:%M"))
            # write current weather to canvas
            offscreen_canvas = addWeather(offscreen_canvas, r)
            
            # if unread messages display notificatoin indicator
            if(len(messages)>2 and message_num<len(messages)):
                continuum += 2
                continuum %= 3 * 255
                red, green, blue = advanceColor(continuum)
                frame_color = graphics.Color(red, green, blue)
                graphics.DrawLine(offscreen_canvas, 1, 0, 31, 0, frame_color)
                graphics.DrawLine(offscreen_canvas, 31, 1, 31, 31, frame_color)
                graphics.DrawLine(offscreen_canvas, 30, 31, 0, 31, frame_color)
                graphics.DrawLine(offscreen_canvas, 0, 30, 0, 0, frame_color)
            display(offscreen_canvas, matrix)
    
        time.sleep(0.05)

except KeyboardInterrupt():
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
