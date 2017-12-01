#!/usr/bin/env python3

import imghdr

import base64
import sys

args = sys.argv[1:]

frames = len(args)

print("Trying to load %d images" % frames)

width = 800
height = 500
fade = 500 #ms
delay = 2000 #ms

dur = (fade + delay) * frames
print("Slideshow will be %d ms" % dur)

f = open('out.svg','w')

f.write('<?xml version="1.0" encoding="utf-8"?>\n')
f.write('<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%d" height="%d" viewBox="0 0 %d %d">\n' % (width, height, width, height))

t = 0

def startImage(path):
  with open(path, "rb") as image_file:
    buf = image_file.read()
    fmt = imghdr.what(None, buf)
    encoded = base64.b64encode(buf)
  f.write('<image opacity="1.0" width="%d" height="%d" xlink:href="data:image/%s;base64,%s">\n' % (width, height, fmt, encoded.decode("utf-8")))

args = args[1:] + [args[0]]

startImage(args[-1])
f.write('</image>\n')

for p in args:

#    <!-- Fallback if animate is not supported -->
#    <image opacity="1.0" width="640" height="480" xlink:href="2017-11-28-235151_648x506_scrot.png">
#    </image>

  print('Adding "%s"' % p)
  #encoded = bytes()

  startImage(p)
  f.write('  <animate attributeName="opacity" attributeType="XML"')
  f.write('                 repeatCount="indefinite"')
  f.write('                 begin="0"')
  f.write('                 dur="%dms"' % dur)
  t += delay
  f.write('                 keyTimes="0;%f;%f;1.0"' % (t / dur, (t + fade) / dur))
  t += fade
  f.write('                 values="0.0;0.0;1.0;1.0"')
  f.write('                 calcMode="linear" />\n')
  f.write('</image>\n')

  print("Processed %d / %d" % (t, dur))

f.write('</svg>')
