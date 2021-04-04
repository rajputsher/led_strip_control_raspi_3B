#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import *
from neopixel import *
import argparse
import sys
import subprocess
import os
import signal
import random as rndm

# LED strip configuration:
LED_COUNT      = 600     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 175     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


options = {
  'off' : [0,0,0],
  'on' : [255,255,255],
  'red' : [255,0,0],
  'lime' : [0,128,0],
  'green' : [0,255,0],
  'blue' : [0,0,255],
  'hblue' : [0,0,128],
  'yellow' : [255,128,0],
  'purple' : [255,0,255],
  'orange' : [255,32,0],
  'warm' : [255,64,16],
  'cool' : [128,128,255],
  'maroon':[128,0,0],
  'pink':[220,20,60],
  'indigo':[75,0,130],
  'teal':[0,128,128],
  'brown':[139,69,19],
  'violet':[138,43,226],
  'gold':[200,150,0],
  'silver':[107,142,35]
}


def randomColor(strip,wait_ms=50):
    strip.setPixelColor(rndm.randint(0,LED_COUNT-1),Color(rndm.randint(0,255), rndm.randint(0,255),rndm.randint(0,255)))
    time.sleep(wait_ms/1000.0)
    strip.show()

def set_color(strip,color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()    

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
        
# Define functions which animate LEDs in various ways.
def twoWayWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i,j in zip(range(strip.numPixels()/2),range(strip.numPixels()/2,-1,-1)) :
        strip.setPixelColor(i, color)
        strip.setPixelColor(j, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

# Define functions which animate LEDs in various ways.
def twoWayWipeRandom(strip,wait_ms=50):
    """Wipe color across display a pixel at a time."""
    color1 = Color(rndm.randint(0,255), rndm.randint(0,255),rndm.randint(0,255))
    color2 = Color(rndm.randint(0,255), rndm.randint(0,255),rndm.randint(0,255))
    for i,j in zip(range(strip.numPixels()),range(strip.numPixels(),-1,-1)) :
        strip.setPixelColor(i, color1)
        strip.setPixelColor(j, color2)
        strip.show()
        time.sleep(wait_ms/1000.0)

# Define functions which animate LEDs in various ways.
def colorWipeAnti(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels(),-1,-1):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

# Main program logic follows:
if __name__ == '__main__':
    #cmd = ['pgrep -f .*python.*strandShiva.py']
    '''
    cmd = ['pgrep -f -l .*strandShiva.py']
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    my_pid, err = process.communicate()
    if len(my_pid.splitlines()) >1:
        for i in range(0,(len(my_pid.splitlines()))):
            if "python" or "sudo" in my_pid.splitlines()[i]:
                strd = 'sudo kill '+my_pid.splitlines()[i]
                print(strd)
                os.system(strd)
    '''
    cmdP = ['pgrep -f -l .*strandShiva.py']
    process = subprocess.Popen(cmdP, shell=True, stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE)
    my_pid, err = process.communicate()
    my_pid = my_pid.decode('utf-8')
    print("len(my_pid.splitlines())",my_pid.splitlines()[1])
    print('my_pid',my_pid)
    print('Number of python:',my_pid.count("python3"))
    print(my_pid.splitlines())
    pyCount = my_pid.count("python3")
    my_pid_app = my_pid.splitlines()
    strApp = []
    for i in range(0,len(my_pid.splitlines())):
       if pyCount == 1:
          break
       strApp.append(my_pid_app[i].split())
       if strApp[i][1] == 'python3':
          strd = 'sudo kill '+strApp[i][0]
          print(strd)
          os.system(strd) 
          pyCount = pyCount-1
          
    print("Options:",''.join(sys.argv[1:]))
    
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    set_color(strip,Color(0,0,0))
    try:
        cmd = ''.join(sys.argv[1:])
        cmd = cmd.lower()
        #print("R:",rgb[1],"G:", rgb[0],"B:",rgb[2])
        while True:
            #set_color(strip, Color(255, 0,0))
            if(cmd in options.keys()):
                rgb = options[cmd]
                set_color(strip, Color(rgb[1], rgb[0],rgb[2]))
                #colorWipe(strip, Color(rgb[1], rgb[0],rgb[2]), 10)
            elif cmd == 'rainbow':
                rainbow(strip)
            elif cmd == 'rainbowcycle':
                rainbowCycle(strip)                
            elif 'chase' in cmd:
                if sys.argv[2]=='rainbow':
                    theaterChaseRainbow(strip,100)
                else:
                    rgb = options[sys.argv[2]]
                    theaterChase(strip, Color(rgb[1], rgb[0],rgb[2]),100)
            elif 'grandrandom' in cmd:
                while True:
                    colorWipe(strip, Color(rndm.randint(0,255), rndm.randint(0,255),rndm.randint(0,255)), 10)
                    colorWipeAnti(strip, Color(rndm.randint(0,255), rndm.randint(0,255),rndm.randint(0,255)), 10)
            elif 'randomwipe' in cmd:
                while True:
                    rgb = rndm.choice(options.values())
                    time.sleep(30)
                    colorWipe(strip, Color(rgb[1], rgb[0],rgb[2]), 10)
                    rgb = rndm.choice(options.values())
                    time.sleep(30)
                    colorWipeAnti(strip, Color(rgb[1], rgb[0],rgb[2]), 10)
            elif 'anticolorwipe' in cmd:
                rgb = options[sys.argv[4]]
                while True:
                    set_color(strip, Color(0,0,0))
                    colorWipe(strip, Color(rgb[1], rgb[0],rgb[2]), 10)
                    set_color(strip, Color(0,0,0))
                    colorWipeAnti(strip, Color(rgb[1], rgb[0],rgb[2]), 10)
            elif 'colorwipe' in cmd:
                rgb = options[sys.argv[3]]
                while True:
                    colorWipe(strip, Color(rgb[1], rgb[0],rgb[2]), 10)
            elif 'twowayrandom' in cmd:
                while True:
                    twoWayWipeRandom(strip,wait_ms=50)
            elif 'twoway' in cmd:
                rgb = options[sys.argv[3]]
                while True:
                    twoWayWipe(strip, Color(rgb[1], rgb[0],rgb[2]), 10)
            elif cmd == 'random':
                while True:
                    randomColor(strip)
            else:
                rgb = options['silver']
                colorWipe(strip, Color(rgb[1], rgb[0],rgb[2]), 10)
                
    except KeyboardInterrupt:
        #if args.clear:
        colorWipe(strip, Color(0,0,0), 10)
