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

# Define functions which animate LEDs in various ways.
def halfhour(strip, wait_ms=100):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()/2):
        a = strip.getPixelColor(i)
        print(i,'-Before: ',strip.getPixelColor(i))
        '''
        strip.setPixelColor(i, Color(0,0,0))
        print(i,'-Flip: ',strip.getPixelColor(i))
        strip.show()
        time.sleep(wait_ms/1000.0)
        strip.setPixelColor(i, a)
        print(i,'-After: ',strip.getPixelColor(i))
        strip.show()
        '''


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
    '''
    cmdP = ['pgrep -f -l .*strandShiva.py']
    process = subprocess.Popen(cmdP, shell=True, stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE)
    my_pid, err = process.communicate()
    #print("len(my_pid.splitlines())",my_pid.splitlines()[1])
    #print('my_pid',my_pid)
    #print('Number of python:',my_pid.count("python"))
    #print(my_pid.splitlines())
    pyCount = my_pid.count("python")
    my_pid_app = my_pid.splitlines()
    strApp = []
    for i in range(0,len(my_pid.splitlines())):
       if pyCount == 1:
          break
       strApp.append(my_pid_app[i].split())
       if strApp[i][1] == 'python':
          strd = 'sudo kill '+strApp[i][0]
          print(strd)
          os.system(strd) 
          pyCount = pyCount-1
    '''      
    print("Options:",''.join(sys.argv[1:]))
    
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    # set_color(strip,Color(0,0,0))
    try:
        cmd = ''.join(sys.argv[1:])
        cmd = cmd.lower()
        #print("R:",rgb[1],"G:", rgb[0],"B:",rgb[2])
        if cmd == 'half':
            halfhour(strip)
        elif cmd == 'full':
            fullhour(strip)
    except KeyboardInterrupt:
        #if args.clear:
        colorWipe(strip, Color(0,0,0), 10)
