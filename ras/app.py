
from gpiozero import LED
from flask import Flask

app = Flask(__name__)
led = LED(12)  # Change this to your GPIO pin number
motion_detected = False  # Flag to track motion detection status


def turn_on_led():
    led.on()


def turn_off_led():
    led.off()


@app.route('/motion-detected', methods=['POST'])
def motion_detected_handler():
    global motion_detected
    motion_detected = True
    turn_on_led()
    return "LED turned on"


@app.route('/motion-not-detected', methods=['POST'])
def motion_not_detected_handler():
    global motion_detected
    motion_detected = False
    turn_off_led()
    return "LED turned off"


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8000)
    finally:
        led.close()
