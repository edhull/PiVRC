# Mobile Virtual Reality Control for Raspberry Pi Camera
### Capgemini, Devoxx London - June 2016
### Installation
(These instructions are most likely incomplete! Personalise/modify them to your setup)

Raspberry Pi's, like all other non-RTOS computers, are at the will and mercy of CPU interrupts. In most cases when working with hardware these interrupts pass harmlessly in the background with no perceptible impact. PWM (Pulse-width modulation) is a concept with predates modern computers and allows digital circuits to emulate analoguous outputs by switching on and off at extremely fast intervals (see further reading). We need software which can borrow one of the Raspberry Pi's dedicated DMA channels to act as a real-time solution to prevent jitter caused by CPU interrupts by other processes (otherwise you'll find that servos will wave around wildly with each round of interrupts). PIGPIO is one of the better solutions that exists:

```sh
$ wget abyz.co.uk/rpi/pigpio/pigpio.zip
$ unzip pigpio.zip
$ cd PIGPIO
$ make -j4
$ sudo make install
```
Make sure you have an up-to-date Python installation

```sh
$ sudo apt-get install python-dev python-pip
```
... and then use Pip to install Flask; a Python-driven webserver (See http://flask.pocoo.org/)
```sh
$ sudo pip install flask
```
Now that we have the infrastructure for controlling servos and displaying webpages, we need the ability stream the Raspberry Pi's camera to the web. 
```sh
$ git clone https://github.com/jacksonliam/mjpg-streamer
```
Compile and build mjpg-streamer following the instructions.
Modify the code below to reflect your home and mjpg-streamer directory, what resolution you want to stream at, and what port you want to use.
```sh
$ echo "killall -s SIGINT mjpg_streamer && /usr/local/bin/mjpg_streamer -o \"/usr/local/lib/mjpg-streamer/output_http.so -w /home/user/mjpg-streamer/www/ -p 1337\" -i \"/usr/local/lib/mjpg-streamer/input_raspicam.so -x 360 -y 360 -fps 15 -ex night -sh 95 -br 55 -awb auto -ev 3 -co 5 -mm matrix \" " > mjpg-streamer.sh
$ chmod +x mjpg-streamer.sh
```
... and then to start streaming the camera. Test this is working by visiting http://*PiIPAddress*:*MJPG-StreamerPort*
```sh
$ ./mjpg-streamer.sh &
```
Or alternatively to run this within a Screen session as a background process:
```sh
$ sudo screen -S camerastreamer -dm bash -c 'python ./mjph-streamer.sh;exec bash'
```
Finally, to run the Flask server and allow the Pi to start streaming camera content and controlling the X/Y servos:
```sh
$ python picam.py &
```
Or alternatively again, within a Screen session:
```sh
$ sudo screen -S python -dm bash -c 'python ./picam.py;exec bash'
```
Tailor these scripts to your circumstance. Ports, GPIO pins, and URLs are extremely likely to need changing.

Picam.py will run the Flask web server, receive mobile telemetry, and translate this into XY rotations for the servos. Whether this will work depends on whether the mobile device accessing the Pi reports alpha/beta/gamma telemetry to a browser client, so make sure to test this (https://developers.arcgis.com/javascript/3/sandbox/sandbox.html?sample=mobile_compass)

If you want to record footage from the camera, you can use Motion.
```sh
$ sudo apt-get install motion
```
... and modify the /etc/motion/motion.conf file to use the camera stream as an input rather than a USB webcam (as well as a bunch of other settings!)

### Hardware
  - No-IR Camera
  - X/Y Camera Servo Platform (http://www.amazon.co.uk/Camera-Platform-Mount-MG90S-Servos/dp/B00BUBDSMA
  - Raspberry Pi

### Dependencies
  - MJPG-Steamer Fork (https://github.com/jacksonliam/mjpg-streamer)
  - Python 2.7+
  - Flask (A micro python-based web server)
  - PIGPIO

### Further reading:

  - https://www.raspberrypi.org/forums/viewtopic.php?t=
  - https://en.wikipedia.org/wiki/Pulse-width_modulation
  - https://w3c.github.io/deviceorientation/spec-source-orientation.html#worked-example
  - https://dev.opera.com/articles/w3c-device-orientation-usage/#practicalconsiderations
  - https://stackoverflow.com/questions/15022630/how-to-calculate-the-angle-from-roational-matrix
  
### Version
v1.0
Ed Hull (05/2016)


