import sys
import signal

# import the library
from gpiozero import LED, MCP3008

if (len(sys.argv) < 3):
    print("Usage: $ sudo blink.py <pin-number> <channel-number>")
    sys.exit(1)

pin = sys.argv[1]
channel = sys.argv[2]
print("Using pin: " + pin)

# Set pin up for output
led = LED(int(pin))
sensor = MCP3008(channel=int(channel))

# I like this, @AndrewS (http://raspi.tv/2016/using-mcp3008-to-measure-temperature-with-gpio-zero-and-raspio-pro-hat)
def check_sensor(gen, threshold=0.5):
    for val in gen:
        print("Reading: {:1f}".format(val))
        yield val > threshold

# main
def main():
    led.source = check_sensor(sensor.values)
    signal.pause()

# boilerplate
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
