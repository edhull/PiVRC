import RPi.GPIO as GPIO
import pigpio
import time
import atexit
from time import sleep
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

GPIO = pigpio.pi()
GPIO.set_servo_pulsewidth(23, 1500) # 
GPIO.set_servo_pulsewidth(24, 1300) # Center the servos


# Cleanup any open objects
def cleanup():
    print ("Cleaning up")
    GPIO.stop()

@socketio.on('connect')
def chat_connect():
    #Send to center positions when a new client connects
    GPIO.set_servo_pulsewidth(24, 1500)
    GPIO.set_servo_pulsewidth(23, 1500)
    print("New Client Connected")

@socketio.on('disconnect')
def chat_disconnect():
    print ("Client disconnected")


@socketio.on('tilted')
def handle_tilt(tiltangle):
    print(tiltangle)


@socketio.on('compassdeg')
def handle_compass(compass):
    if (compass > 100.0) and (compass < 260.0):
        GPIO.set_servo_pulsewidth(24, scale(compass, (100.0, 260.0), (1050,1950)))

@socketio.on('tiltdeg')
def handle_rotation(tilt):
    GPIO.set_servo_pulsewidth(23, scale(tilt, (180.0, 0.0), (1000,2000)))

# Load the main form template on webrequest for the root page
@app.route("/")
def main():
    templateData = {
        'title' : 'Camera'
        }
    # Pass the template data into the template picam.html and return it to the user
    return render_template('picam.html', **templateData)

def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst
    eg print scale(50, (0.0, 100.0), (-1.0, +1.0)) would return 0
    """
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

# Clean everything up when the app exits
atexit.register(cleanup)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=80)
