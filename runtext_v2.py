#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time

options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'


matrix = RGBMatrix(options = options)
offscreen_canvas = matrix.CreateFrameCanvas()
font = graphics.Font()
font.LoadFont("../../../fonts/7x13.bdf")
textColor = graphics.Color(255, 255, 0)
pos = offscreen_canvas.width
        

try:
    message = "hello there"
    while True:
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, message)
        pos -= 1
        if (pos + len < 0):
            pos = offscreen_canvas.width

        time.sleep(0.05)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
except KeyboardInterrupt():
    sys.exit(0)

