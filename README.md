# Control for WS2812 LEDs using Raspberry Pi- Model 3B

This repository is copy of the work represented in this [tutorial](https://tutorials-raspberrypi.de/raspberry-pi-ws2812-ws2811b-rgb-led-streifen-steuern/).

Documenting here  the main steps to re-use in the future.

Pre-Steps:

1. `sudo apt-get update`
2. Install required packages:<br/> `sudo apt-get install gcc make build-essential python-dev git scons swig`
3. Deactivate the audio output by editing the snd-backlist.conf file:<br/>
   `sudo nano /etc/modprobe.d/snd-blacklist.conf` <br/>Add this line to the file: `blacklist snd_bcm2835`
4. We also need to edit the configuration file:<br/>`sudo nano /boot/config.txt`<br/>
Below are lines with the following content (you can search with CTRL + W):
    ```
    #Enable audio (loads snd_bcm2835)
    dtparam = audio = on
    ```
    This lower line is commented out with a hash / hashtag # at the beginning of the line:#dtparam=audio=on
5. Restart the pi : `sudo reboot`

Working with repo: 

1. Go to rpi_ws281x, and run scons, this will create the necessary object files to link during build.
   ```
   cd rpi_ws281x/
   sudo scons
   ```
2. Go to python folder
   ```
   cd python
   ```
3. Install the library
   ```
    sudo python3 setup.py build
    sudo python3 setup.py install
    sudo pip3 install adafruit-circuitpython-neopixel
   ```
4. Test by running files in examples folder:
    ```
    sudo python3 examples/strandtest.py
    ```

