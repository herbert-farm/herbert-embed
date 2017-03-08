
import sys
import time

# import the library
from gpiozero import LED

if (len(sys.argv) < 2):
    print("Usage: $ sudo blink.py <pin-number>")
    sys.exit(1)

pin = sys.argv[1]
print("Using pin: " + pin)

# Set pin up for output
led = LED(int(pin))

# main
def main():
    while True: 5
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
