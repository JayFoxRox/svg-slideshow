#!/usr/bin/env python3

import imghdr
import argparse
import base64
from xml.etree import ElementTree as tree
from PIL import Image


def init_parser():
    parser = argparse.ArgumentParser(description="Utility to generate animated SVGs for a slideshow from images")
    parser.add_argument('files', nargs='+')
    parser.add_argument('-x', '--width', type=int, default=800, help='output image width in pixels (default: 800)')
    parser.add_argument('-y', '--height', type=int, default=500, help='output image height in pixels (default: 500)')
    parser.add_argument('-f', '--fade', type=int, default=500, help='duration of fade in milliseconds (default: 500)')
    parser.add_argument('-d', '--delay', type=int, default=2000, help='duration of each image shown between fades in milliseconds (default: 2000)')
    parser.add_argument('-o', '--outfile', type=str, default='out.svg', help='path to output file (default: out.svg)')
    return parser


def add_image(img):
    with open(img, "rb") as image_file:
        buf = image_file.read()
        fmt = imghdr.what(None, buf)
        encoded = base64.b64encode(buf)
        image = tree.SubElement(svg, 'image', opacity='1.0', width=str(w), height=str(h))
        image.set(u'xlink:href', u"data:image/%s;base64,%s" % (fmt, encoded.decode("utf-8")))
        return image


if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args()

    frames = len(args.files)
    print("Trying to load %d images" % frames)

    w = args.width
    h = args.height
    fade = args.fade
    delay = args.delay
    dur = (fade + delay) * frames

    print("Slideshow will be %d ms" % dur)

    with open(args.outfile, 'w') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        svg = tree.Element('svg', width=str(w), height=str(h), version='1.1', xmlns='http://www.w3.org/2000/svg',
                           viewBox='0 0 %d %d' % (w, h))
        svg.set(u'xmlns:xlink', u'http://www.w3.org/1999/xlink')

        add_image(args.files[0])
        # append first image to back of list for a smooth transition
        args.files.append(args.files.pop(0))
        t = 0
        for img in args.files:
            print('Adding "%s"' % img)
            t += delay
            image = add_image(img)
            animate = tree.SubElement(image, 'animate', attributeName='opacity', attributeType='XML',
                                      repeatCount='indefinite', begin='0', dur='%dms' % dur,
                                      keyTimes= "0.0;%f;%f;1.0" % (t/dur, (t + fade)/dur),
                                      values="0.0;0.0;1.0;1.0", calcMode='linear')
            t += fade

        f.write(tree.tostring(svg, encoding="unicode"))
