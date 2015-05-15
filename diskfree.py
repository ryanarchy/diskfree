#!/usr/bin/env python

import subprocess
from PIL import Image, ImageDraw, ImageFont

XRES = 1920
YRES = 1080
CENTER = (XRES/2, YRES/2)
DEVICE = "/dev/sda1"
CIRCLE_RADIUS = 450
CIRCLE_BOUNDING = (CENTER[0] - CIRCLE_RADIUS, CENTER[1] - CIRCLE_RADIUS, CENTER[0] + CIRCLE_RADIUS, CENTER[1] + CIRCLE_RADIUS)
TARGET_FILENAME = "diskfree.jpg"
TARGET_PATH = "."


df = subprocess.Popen(["df", "/dev/sda1"], stdout=subprocess.PIPE)

output = df.communicate()[0]

device, size, used, available, percent, mountpoint = output.split("\n")[1].split()

pieArc = int((float(percent[:-1])/100) * 360)

# set up our font for use
font = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSans.ttf", 24)

im = Image.new("RGB", (XRES, YRES), "black")
draw = ImageDraw.Draw(im)
outputText = percent + " used on device " + DEVICE
textXOffset = CENTER[0] - (font.getsize(outputText)[0]/2)
textYOffset = YRES - font.getsize(outputText)[1]
draw.text((textXOffset, textYOffset), outputText, font=font)
draw.ellipse(CIRCLE_BOUNDING, fill="green")
draw.pieslice(CIRCLE_BOUNDING, 0, pieArc, fill="red")
im.save(mountpoint + "/" + TARGET_FILENAME)
