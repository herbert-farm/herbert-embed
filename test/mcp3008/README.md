# test/mcp3008/mcp3008.py

## Purpose

This test program and circuit reads the signal coming from the MCP3008 ADC and turns an LED on if it passes 1/2 of the max signal value.

## Usage

To use this script, connect the reference circuit specified in `blink_ckt.png`, where:

* __VI1__ goes to any Pi GPIO pin (recommended is pin 27)
* __VI2__ goes to the sensor you're measuring

```bash
$ sudo python3 ./mcp3008.py 27 0 # or whatever pin, channel you used
```
