

import sys
import time

# import the library
import RPi.GPIO as GPIO

# Set the pinmode to Raspi-specified pinout
GPIO.setMode(GPIO.BOARD)


if (sys.argv < 2):
    print("Usage: $ sudo blink.py <pin-number>")

pin = sys.argv[2]
print("Using pin: " + pin)

# Set pin up for output
GPIO.setup(pin, GPIO.OUT)

# main
def main():

    while True:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(1)


# boilerplate
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
