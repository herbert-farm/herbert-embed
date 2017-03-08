

import sys
import time

# import the library
from gpiozero import LED


if (sys.argv < 2):
    print("Usage: $ sudo blink.py <pin-number>")

pin = sys.argv[2]
print("Using pin: " + pin)

# Set pin up for output
led = LED(pin)

# main
def main():
    while True:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)

# boilerplate
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
