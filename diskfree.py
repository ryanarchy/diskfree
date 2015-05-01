#!/usr/bin/env python

import subprocess
import Image, ImageDraw

XRES = 1920
YRES = 1080
CENTER = (XRES/2, YRES/2)
DEVICE = "/dev/sda1"
CIRCLE_RADIUS = 450
CIRCLE_BOUNDING = (CENTER[0] - CIRCLE_RADIUS, CENTER[1] - CIRCLE_RADIUS, CENTER[0] + CIRCLE_RADIUS, CENTER[1] + CIRCLE_RADIUS)
TARGET_FILE = "diskfree.jpg"


df = subprocess.Popen(["df", "/dev/sda1"], stdout=subprocess.PIPE)

output = df.communicate()[0]

device, size, used, available, percent, mountpoint = output.split("\n")[1].split()

pieArc = int((float(percent[:-1])/100) * 360)


im = Image.new("RGB", (XRES, YRES), "black")
draw = ImageDraw.Draw(im)
outputText = percent + " used on device " + DEVICE
textXOffset = CENTER[0] - (draw.textsize(outputText)[0]/2)
textYOffset = YRES - draw.textsize(outputText)[1]
draw.text((textXOffset, textYOffset), outputText)
draw.ellipse(CIRCLE_BOUNDING, fill="green")
draw.pieslice(CIRCLE_BOUNDING, 0, pieArc, fill="red")
im.save(mountpoint + "/" + TARGET_FILE, "JPEG")
